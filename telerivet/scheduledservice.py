
from .entity import Entity

class ScheduledService(Entity):
    """
    Represents a scheduled service within Telerivet.
    
    Scheduled services allow services to be triggered automatically at specified
    times.
    The ScheduledService object is only used for services that are triggered for
    a project (e.g. `scheduled_actions` or `scheduled_script`).
    
    Note: To schedule services that are triggered for a contact, the
    [ScheduledMessage](#ScheduledMessage) object should be used instead, with
    `message_type`=`service`.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the scheduled service
          * Read-only
      
      - service_id (string, max 34 characters)
          * ID of the service to be triggered
          * Read-only
      
      - rrule
          * Recurrence rule for recurring scheduled services, e.g. 'FREQ=MONTHLY' or
              'FREQ=WEEKLY;INTERVAL=2'; see
              [RFC2445](https://tools.ietf.org/html/rfc2445#section-4.3.10).
          * Updatable via API
      
      - timezone_id
          * Timezone ID used to compute times for recurring scheduled services; see [List of tz
              database time zones Wikipedia
              article](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
          * Updatable via API
      
      - time_created (UNIX timestamp)
          * Time the scheduled service was created in Telerivet
          * Read-only
      
      - start_time (UNIX timestamp)
          * The time that the service will be triggered (or first triggered for recurring
              scheduled services)
          * Updatable via API
      
      - end_time (UNIX timestamp)
          * Time after which a recurring scheduled service will stop (not applicable to
              non-recurring scheduled services)
          * Updatable via API
      
      - prev_time (UNIX timestamp)
          * The most recent time that Telerivet triggered this scheduled service (null if it has
              never been triggered)
          * Read-only
      
      - next_time (UNIX timestamp)
          * The next upcoming time that Telerivet will trigger this scheduled service (null if
              it will not be triggered again)
          * Read-only
      
      - occurrences (int)
          * Number of times this scheduled service has already been triggered
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this scheduled service. Variable names may be up to 32
              characters in length and can contain the characters a-z, A-Z, 0-9, and _.
              Values may be strings, numbers, or boolean (true/false).
              String values may be up to 4096 bytes in length when encoded as UTF-8.
              Up to 100 variables are supported per object.
              Setting a variable to null will delete the variable.
          * Updatable via API
      
      - project_id
          * ID of the project this scheduled service belongs to
          * Read-only
    """

    def save(self):
        """
        Saves any fields or custom variables that have changed for this scheduled service.
        """
        super(ScheduledService, self).save()

    def delete(self):
        """
        Cancels this scheduled service.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/scheduled_services/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
