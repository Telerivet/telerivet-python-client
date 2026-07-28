
from .entity import Entity

class StoredFile(Entity):
    """
    Represents a file stored in a Telerivet project, such as a media attachment for outgoing
    messages.
    
    Stored files are also automatically created for media attachments for
    incoming messages.
    
    Files can be uploaded via [project.uploadFile](#Project.uploadFile), then
    attached to outgoing messages by passing the file ID as a `file_id` item in the `media`
    parameter when sending a message or broadcast.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the stored file
          * Read-only
      
      - filename (string, max 127 characters)
          * Filename of the stored file
          * Updatable via API
      
      - type
          * MIME type of the file
          * Read-only
      
      - size (int)
          * Size of the file in bytes
          * Read-only
      
      - description (string, max 1000 characters)
          * Description of the file
          * Updatable via API
      
      - category
          * Category of the stored file
          * Allowed values: outgoing_media, incoming_media, call_audio, test_recording,
              script_module, icon
          * Read-only
      
      - source
          * How the stored file was created
          * Allowed values: upload, recording, message, api
          * Read-only
      
      - message_id
          * ID of the message associated with this file, if any. Files associated with a message
              are deleted automatically when the message is deleted.
          * Read-only
      
      - sha256
          * SHA-256 hash of the file content (lowercase hex), if available
          * Read-only
      
      - time_created (UNIX timestamp)
          * Time the file was created in Telerivet
          * Read-only
      
      - user_id (string, max 34 characters)
          * ID of the Telerivet user who created the file (if applicable)
          * Read-only
      
      - url
          * URL where the file content can be downloaded. Note: this URL is temporary and may
              not be valid for more than 1 day; retrieve the stored file again to get a fresh URL.
          * Read-only
      
      - thumbnail_url
          * URL of a thumbnail image for video files, if available. Note: this URL is temporary
              and may not be valid for more than 1 day.
          * Read-only
      
      - project_id
          * ID of the project this file belongs to
          * Read-only
    """

    def save(self):
        """
        Saves any fields that have changed for this stored file.
        """
        super(StoredFile, self).save()

    def delete(self):
        """
        Deletes this stored file.
        
        A stored file may only be deleted by the user who created it or by a
        project administrator, and may not be deleted while it is attached to an existing message.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/files/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
