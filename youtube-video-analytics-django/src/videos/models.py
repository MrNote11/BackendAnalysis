"""
Models for video analytics application.
Includes custom TimescaleDB model base class.
"""
import uuid
from django.db import models, connection
from django.utils import timezone


class TimescaleModel(models.Model):
    """
    Abstract base class for TimescaleDB hypertables.
    Automatically creates hypertables with compression settings.
    """
    time = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['-time']
    
    @classmethod
    def create_hypertable(cls):
        """
        Creates a TimescaleDB hypertable from a regular table.
        Should be called after migrations.
        """
        table_name = cls._meta.db_table
        chunk_interval = getattr(cls, 'CHUNK_TIME_INTERVAL', '7 days')
        
        with connection.cursor() as cursor:
            # Create hypertable
            cursor.execute(f"""
                SELECT create_hypertable(
                    '{table_name}', 
                    'time', 
                    chunk_time_interval => INTERVAL '{chunk_interval}',
                    if_not_exists => TRUE
                );
            """)
            
            # Enable compression if specified
            if getattr(cls, 'ENABLE_COMPRESSION', False):
                compress_orderby = getattr(cls, 'COMPRESS_ORDERBY', 'time DESC')
                compress_segmentby = getattr(cls, 'COMPRESS_SEGMENTBY', None)
                
                cursor.execute(f"""
                    ALTER TABLE {table_name} SET (
                        timescaledb.compress,
                        timescaledb.compress_orderby = '{compress_orderby}'
                        {f", timescaledb.compress_segmentby = '{compress_segmentby}'" if compress_segmentby else ''}
                    );í
                """)
                
                # Add compression policy
                drop_after = getattr(cls, 'DROP_AFTER', '1 year')
                cursor.execute(f"""
                    SELECT add_compression_policy('{table_name}', INTERVAL '7 days');
                """)
                
                # Add retention policy
                cursor.execute(f"""
                    SELECT add_retention_policy('{table_name}', INTERVAL '{drop_after}');
                """)


# Watch Sessions App Models
class WatchSession(TimescaleModel):
    """
    Tracks user watch sessions for video analytics.
    Each session represents a unique viewing instance.
    """
    watch_session_id = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        db_index=True,
        editable=False
    )
    path = models.CharField(max_length=500, blank=True, default='', db_index=True)
    referer = models.CharField(max_length=500, blank=True, default='', db_index=True)
    video_id = models.CharField(max_length=100, blank=True, default='', db_index=True)
    last_active = models.DateTimeField(default=timezone.now)
    
    # TimescaleDB configuration
    CHUNK_TIME_INTERVAL = '30 days'
    DROP_AFTER = '3 years'
    
    class Meta:
        db_table = 'watch_sessions'
        indexes = [
            models.Index(fields=['watch_session_id']),
            models.Index(fields=['video_id']),
        ]
    
    def __str__(self):
        return f"WatchSession {self.watch_session_id} - {self.video_id}"


# Video Events App Models
class YouTubeWatchEvent(TimescaleModel):
    """
    Records individual watch events from YouTube player.
    Tracks playback state, position, and user interaction.
    """
    is_ready = models.BooleanField(default=False)
    video_id = models.CharField(max_length=100, db_index=True)
    video_title = models.CharField(max_length=500)
    current_time = models.FloatField(help_text="Current playback position in seconds")
    video_state_label = models.CharField(max_length=50, db_index=True)
    video_state_value = models.IntegerField()
    referer = models.CharField(max_length=500, blank=True, default='', db_index=True)
    watch_session_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # TimescaleDB configuration
    CHUNK_TIME_INTERVAL = '7 days'
    DROP_AFTER = '1 year'
    ENABLE_COMPRESSION = True
    COMPRESS_ORDERBY = 'time DESC'
    COMPRESS_SEGMENTBY = 'video_id'
    
    class Meta:
        db_table = 'youtube_watch_events'
        indexes = [
            models.Index(fields=['video_id', 'time']),
            models.Index(fields=['watch_session_id']),
            models.Index(fields=['video_state_label']),
        ]
    
    def __str__(self):
        return f"Event {self.id} - {self.video_id} at {self.current_time}s"