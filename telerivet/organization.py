
from .entity import Entity

class Organization(Entity):
    """
    Represents a Telerivet organization.
    
    Fields:
    
      - id (string, max 34 characters)
          * ID of the organization
          * Read-only
      
      - name
          * Name of the organization
          * Updatable via API
      
      - timezone_id
          * Billing quota time zone ID; see
              <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>
          * Updatable via API
    """

    def save(self):
        """
        Saves any fields that have changed for this organization.
        """
        super(Organization, self).save()

    def getBillingDetails(self):
        """
        Retrieves information about the organization's service plan and account balance.
        
        Returns:
            (associative array)
              - balance (string)
                  * Prepaid account balance
              
              - balance_currency (string)
                  * Currency of prepaid account balance
              
              - plan_name (string)
                  * Name of service plan
              
              - plan_price (string)
                  * Price of service plan
              
              - plan_currency (string)
                  * Currency of service plan price
              
              - plan_rrule (string)
                  * Service plan recurrence rule (e.g. FREQ=MONTHLY or FREQ=YEARLY)
              
              - plan_paid (boolean)
                  * true if the service plan has been paid for the current billing interval; false
                      if it is unpaid (free plans are considered paid)
              
              - plan_start_time (UNIX timestamp)
                  * Time when the current billing interval started
              
              - plan_end_time (UNIX timestamp)
                  * Time when the current billing interval ends
              
              - plan_suspend_time (UNIX timestamp)
                  * Time when the account will be suspended, if the plan remains unpaid after
                      `plan_end_time` (may be null)
              
              - plan_limits (dict)
                  * Object describing the limits associated with the current service plan. The
                      object contains the following keys: `phones`, `projects`, `active_services`,
                      `users`, `contacts`, `messages_day`, `stored_messages`, `data_rows`,
                      `api_requests_day`. The values corresponding to each key are integers, or null.
              
              - recurring_billing_enabled (boolean)
                  * True if recurring billing is enabled, false otherwise
              
              - auto_refill_enabled (boolean)
                  * True if auto-refill is enabled, false otherwise
        """
        data = self._api.doRequest("GET", self.getBaseApiPath() + "/billing")
        return data

    def getUsage(self, usage_type):
        """
        Retrieves the current usage count associated with a particular service plan limit. Available
        usage types are `phones`, `projects`, `users`, `contacts`, `messages_day`,
        `stored_messages`, `data_rows`, and `api_requests_day`.
        
        Arguments:
          - usage_type
              * Usage type.
              * Required
          
        Returns:
            int
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/usage/%s" % (usage_type))

    def queryProjects(self, **options):
        """
        Queries projects in this organization.
        
        Arguments:
            
            - name
                * Filter projects by name
                * Allowed modifiers: name[ne], name[prefix], name[not_prefix], name[gte], name[gt],
                    name[lt], name[lte]
            
            - sort
                * Sort the results based on a field
                * Allowed values: default, name
                * Default: default
            
            - sort_dir
                * Sort the results in ascending or descending order
                * Allowed values: asc, desc
                * Default: asc
            
            - page_size (int)
                * Number of results returned per page (max 500)
                * Default: 50
            
            - offset (int)
                * Number of items to skip from beginning of result set
                * Default: 0
          
        Returns:
            APICursor (of Project)
        """
        from .project import Project
        return self._api.newApiCursor(Project, self.getBaseApiPath() + "/projects", options)

    def getBaseApiPath(self):
        return "/organizations/%(id)s" % {'id': self.id} 
