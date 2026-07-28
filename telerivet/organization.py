
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
          * Billing quota time zone ID; see [List of tz database time zones Wikipedia
              article](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
          * Updatable via API
    """

    def createProject(self, **options):
        """
        Creates a new project.
        
        Some project settings are not currently possible to configure via
        the API, and can only be edited via the web app after the project is created.
        
        Arguments:
              * Required
            
            - name (string)
                * Name of the project to create, which must be unique in the organization.
                * Required
            
            - timezone_id
                * Default TZ database timezone ID; see [List of tz database time zones Wikipedia
                    article](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones). This timezone
                    is used when computing statistics by date.
            
            - url_slug
                * Unique string used as a component of the project's URL in the Telerivet web app
                    (required length: 3-18 characters). If not provided, a URL slug will be generated
                    automatically.
            
            - auto_create_contacts (bool)
                * If true, a contact will be automatically created for each unique phone number that
                    a message is sent to or received from. If false, contacts will not automatically be
                    created (unless contact information is modified by an automated service). The
                    Conversations tab in the web app will only show messages that are associated with a
                    contact.
                * Default: 1
            
            - message_retention_days (int)
                * Number of days to retain messages in this project. Messages older than this will
                    be automatically deleted. If null or not provided, messages will be retained
                    forever.
            
            - short_link_scheme (bool)
                * If true (the default), short links in messages will include the scheme (e.g.,
                    'https://rvt.me/xxxxxxxxx'). If false, short links will not include the scheme
                    (e.g., 'rvt.me/xxxxxxxxx').
                * Default: 1
            
            - vars
                * Custom variables and values to set for this project
          
        Returns:
            Project
        """
        from .project import Project
        return Project(self._api, self._api.doRequest("POST", self.getBaseApiPath() + "/projects", options))

    def save(self):
        """
        Saves any fields that have changed for this organization.
        """
        super(Organization, self).save()

    def getBillingDetails(self, **options):
        """
        Retrieves information about the organization's service plan, including pricing, billing
        period, current limits, enabled features, overage rates, and any minimum usage fees, as well
        as the current account balance and payment status.
        
        The `plan_limits` object specifies the maximum allowed usage per
        metric (e.g. messages per day, contacts, API requests per day) that is included as part of
        the `plan_price`. Unless otherwise specified, each limit is the total across all projects in
        the organization (except for `custom_actions`).
        
        When usage reaches a limit, what happens depends on the metric
        and whether the `soft_limits` feature is enabled in `plan_features`. For some limits,
        additional usage is allowed and is billed based on `overage_rates` when the `soft_limits`
        feature is enabled. For other limits, additional usage is blocked until the plan is upgraded
        to increase the limits.
        
        Additional details about how service plan limits are defined,
        including what happens when the limits are reached, can be found in the [User
        Guide](https://guide.telerivet.com/hc/en-us/articles/360038959631-Service-Plan-Limits).
        
        Arguments:
            
            - usage (bool)
                * If true, the response also includes a `usage` object with the current usage count
                    for every key in `plan_limits` — equivalent to calling `getUsage` once per key but
                    in the same round-trip. Omit (or pass false) to skip the usage counters.
                * Default:
          
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
                      values are integers, or null. Either `external_messages_day` or
                      `external_messages_period` is included depending on the organization's billing
                      mode (per-day vs. per-plan-period messaging quota). Each key:
                      
                      - `contacts`: Stored contacts — The maximum number of contacts stored in your
                      contact database at any time. Each contact can have a name, phone number, and up
                      to 100 custom fields, and can be added to groups. By default, a contact is
                      automatically created for each phone number you communicate with, as long as there
                      is space in your contact database. Automatic contact creation can be disabled in
                      the project settings if you don't need to store contacts. You can send messages to
                      an unlimited number of different phone numbers if you don't store them in your
                      contact database.
                      - `phones`: Routes — The maximum number of different routes that your
                      organization uses to send or receive messages through Telerivet, including Android
                      phones, virtual numbers, alphanumeric sender IDs, SMS shortcodes, and integrations
                      with chat apps like WhatsApp. On service plans that support multiple routes, you
                      can distribute messages among different routes for higher volume, geographic
                      reach, or better rates.
                      - `active_services`: Active automated services — The number of automated
                      services that run in response to certain events, such as when a new message is
                      received, when a message's status changes, or when triggered by a user. Common
                      types of automations like polls and auto-replies can be created from built-in
                      templates. Custom actions can be created using a drag-and-drop flow builder,
                      JavaScript, or a webhook.
                      - `users`: User logins — The maximum number of user accounts you can add for
                      people in your organization to log in and use Telerivet. Each user account can
                      have its own permissions.
                      - `stored_messages`: Stored messages — The total number of messages stored in
                      your Telerivet account, including scheduled messages. You can delete old or
                      unneeded messages to stay under this limit.
                      - `service_invocations_day`: Daily service invocations — The maximum number of
                      times automated services can run per day, excluding Webhook API services. This
                      includes service rules triggered by incoming messages, scheduled triggers, and
                      manual invocations. The counter resets at midnight in your organization's
                      timezone.
                      - `api_requests_day`: Daily API requests — The maximum number of API requests
                      your organization can make per day, counting both REST API and Webhook API
                      requests. The quota resets daily at midnight in the organization's time zone. If
                      you pay Telerivet directly for each message, REST API requests to send messages,
                      and Webhook API requests to receive notifications of incoming messages and
                      delivery reports, are exempt from this limit.
                      - `projects`: Projects — Each project represents an independent mobile messaging
                      system. Each project has its own messages, contacts, routes, and services, and its
                      own set of user permissions. If necessary, you can add multiple projects under one
                      organization and one billing plan.
                      - `data_rows`: Rows in custom data tables — Custom data tables are used to store
                      responses to polls and other automated services. You can also import your own data
                      to build data-driven automations.
                      - `script_module_mb`: Cloud Script module storage quota (MB) — Storage quota for
                      Cloud Script modules — code modules that you push to Telerivet to run as part of
                      automated services. Measured as the total size of all module files across the
                      organization.
                      - `stored_file_mb`: File storage quota (MB) — Storage quota for files uploaded
                      to Telerivet, including media attachments sent or received in messages.
                      - `custom_actions`: Custom actions per service — The maximum number of custom
                      actions or conditions allowed per automated service. Custom actions extend
                      services with logic written in a drag-and-drop flow builder, JavaScript, or
                      webhooks. Plans with the Advanced Automation feature have no per-service limit.
                      - `groups`: Contact groups — The maximum number of contact groups. Groups are
                      used to organize contacts and to send messages to many recipients at once.
                      - `custom_contact_fields`: Custom contact fields — The maximum number of custom
                      fields that can be defined for contacts. Custom fields store extra information
                      about contacts beyond the built-in name and phone number — for example, an
                      account ID, language preference, or any project-specific attribute.
                      - `external_messages_day`: Included Messages/Day - Bring Your Own Connectivity —
                      The maximum number of messages that can be sent or received per day when using
                      your own connectivity provider or an Android phone with the Telerivet Gateway app
                      (not when paying Telerivet for each message). The counter resets at midnight in
                      your organization's timezone. This limit applies when the plan's billing mode has
                      a per-day messaging quota.
                      - `external_messages_period`: Included Messages/Plan Period - Bring Your Own
                      Connectivity — The maximum number of messages that can be sent or received per
                      plan period (typically monthly or yearly) when using your own connectivity
                      provider or an Android phone with the Telerivet Gateway app (not when paying
                      Telerivet for each message). This limit applies when the plan has a
                      per-plan-period messaging quota. Each sent or received SMS message part, voice
                      call, USSD session, chat app message, or MMS message is counted as one message;
                      multi-part SMS messages are counted based on the number of SMS parts in the
                      message.
                      - `ai_chat_credits_day`: AI chat credits/day
              
              - plan_features (dict)
                  * Object describing which platform features are enabled for this organization. The
                      keys are string feature IDs and the values are booleans. Available features:
                      
                      - `direct_connectivity`: Direct Connectivity — Use Telerivet-managed phone
                      routes where Telerivet handles billing with upstream messaging gateways on your
                      behalf, instead of requiring you to bring your own gateway credentials.
                      - `airtime_transfer`: Airtime Topup & Transfer — Send airtime to prepaid mobile
                      phones as a reward or participation incentive, or top-up the airtime on your own
                      SIM card directly from Telerivet. (Requires Pro plan or above)
                      - `click_tracking`: Click Tracking — Shorten links and track which contacts
                      clicked a link in your message.
                      - `custom_gateway`: Custom Gateways — Integrate with an SMS shortcode or another
                      gateway API. Telerivet can integrate with both HTTP or SMPP messaging APIs, and
                      can configure VPN connections directly with mobile networks if necessary.
                      (Integration fee varies depending on API - contact us)
                      - `custom_logo`: Custom Logo — Replace the Telerivet logo in the web app with
                      your own logo. (Requires Pro plan or above)
                      - `custom_domain`: Custom Domain Name — Access your Telerivet account from your
                      own domain name like sms.example.com, and hide Telerivet branding from users.
                      Configure a custom domain for branded short links. (Contact us for pricing)
                      - `soft_limits`: Soft Limits — Allow exceeding your plan's daily, monthly, or
                      annual limits by paying for extra messages, API requests, or service invocations.
                      - `auto_resend`: Automatic Message Resend & Failover — Configure custom rules to
                      automatically resend failed messages and failover between routes. (Requires plan
                      with Advanced custom automation)
                      - `export_storage`: Cloud Data Export — Automatically export and backup
                      messages, contacts, and other data to the cloud. Connect your own Amazon Web
                      Services S3 account for data storage. (Requires plan with Advanced custom
                      automation)
                      - `static_ip_address`: Static IP Address — Configure Telerivet to use a static
                      IP address for outbound HTTP requests if you need to allow inbound traffic from
                      specific IP addresses in your firewall. (Requires plan with Advanced custom
                      automation)
                      - `script_modules`: Cloud Script Modules — Run Cloud Script API code from an
                      external codebase hosted on GitHub, or push code to Telerivet directly from your
                      development environment. Use source control to track version history. (Requires
                      plan with Advanced custom automation)
                      - `service_templates`: Service Templates — Create reusable automated services
                      that can be shared with multiple projects and organizations. (Contact us for
                      pricing)
                      - `single_sign_on`: SAML Single Sign-On — Allow users to log in via your
                      organization's single sign-on identity provider (SAML 2.0). (Contact us for
                      pricing)
                      - `contact_sync`: Contact Data Sync — Synchronize contact information and
                      opt-out status across multiple Telerivet projects. (Requires Growth plan or above)
                      - `external_airtime_providers`: External Airtime Providers — Configure airtime
                      providers in your projects using your own credentials with an external airtime
                      provider, in addition to (or instead of) Telerivet-managed airtime.
                      - `wire_payments`: Wire Payments — Pay Telerivet invoices via bank wire transfer
                      in addition to credit card and other online payment methods.
                      - `custom_dashboards`: Custom Dashboards — Create custom dashboards with charts
                      and metrics showing Telerivet usage and providing business intelligence about the
                      results of your campaigns. (Requires Pro plan or above)
                      - `branded_short_links`: Branded Short Links — Configure a custom domain name
                      for short links, instead of using the default domain (rvt.me). (Requires Growth
                      plan or above)
                      - `custom_solutions`: Custom Solution Development — Work with Telerivet's
                      professional services team to implement a custom solution for your business needs.
                      (Contact us for pricing)
              
              - overage_rates (dict)
                  * Per-unit overage rates billed when usage exceeds the corresponding plan limit.
                      Only present when the `soft_limits` feature is enabled in `plan_features` —
                      without `soft_limits`, reaching a limit blocks further usage until the counter
                      resets rather than accruing per-unit charges, so the rates would not apply and the
                      field is omitted entirely. When present, each entry is an object with `amount` and
                      `currency` properties, where `amount` is the positive per-unit cost in `currency`,
                      or null if no rate is configured. Keys:
                      
                      - `message`: Cost per external (bring your own connectivity) message sent or
                      received beyond the daily limit (`plan_limits.external_messages_day`) or
                      per-period limit (`plan_limits.external_messages_period`).
                      - `api_request`: Cost per REST API request beyond `plan_limits.api_requests_day`.
                      - `service_invocation`: Cost per automated-service invocation beyond
                      `plan_limits.service_invocations_day`.
              
              - minimum_usage_fees (array)
                  * Array of minimum usage fees configured for this organization. Each fee
                      guarantees a minimum amount of usage-based billing per billing cycle (the period
                      from `plan_start_time` to `plan_end_time`, recurring per `plan_rrule`) for a
                      particular set of usage categories — for example, a monthly minimum on
                      per-message fees via a particular provider. If the actual usage-based charges
                      across the fee's categories add up to less than the minimum during a billing
                      cycle, the shortfall is billed up to the minimum amount, and added to the
                      organization's recurring billing alongside the plan price. If actual usage exceeds
                      the minimum, no additional minimum-usage charge is applied for that cycle. The
                      array is empty when no minimum usage fees are configured.
              
              - recurring_billing_enabled (boolean)
                  * True if recurring billing is enabled, false otherwise
              
              - auto_refill_enabled (boolean)
                  * True if auto-refill is enabled, false otherwise
              
              - usage (dict)
                  * Object mapping each `plan_limits` key to the current integer usage count for
                      that metric — present only when the request was made with `usage=true`. Includes
                      either `external_messages_day` or `external_messages_period` (matching whichever
                      the organization's billing mode produces in `plan_limits`), not both. Reset
                      schedules and the per-service `custom_actions` semantics described on
                      [getUsage](#Organization.getUsage) apply here as well.
        """
        data = self._api.doRequest("GET", self.getBaseApiPath() + "/billing", options)
        return data

    def getUsage(self, usage_type):
        """
        Retrieves the current usage count associated with a particular service plan limit.
        
        The available `usage_type` values are the same as the keys returned
        in `plan_limits` from the [getBillingDetails](#Organization.getBillingDetails) method, so
        each call returns the current value of the corresponding limit's counter.
        
        Notes:
        
        - `external_messages_day` and `external_messages_period` reset on
        different schedules: daily counters reset at midnight in the organization's timezone; period
        counters reset at the start of the next plan period (`plan_start_time` to `plan_end_time`
        from `getBillingDetails`).
        - `custom_actions` is the highest custom-action count across any
        single active service in the organization (since the corresponding limit is enforced per
        service, not per organization).
        - `messages_day` is retained as a deprecated alias for
        `external_messages_day`
        
        Arguments:
          - usage_type
              * Usage type. Same as the keys returned in `plan_limits` from
                  `Organization.getBillingDetails`.
              * Allowed values: contacts, phones, active_services, users, stored_messages,
                  service_invocations_day, api_requests_day, projects, data_rows, script_module_mb,
                  stored_file_mb, custom_actions, groups, custom_contact_fields, external_messages_day,
                  external_messages_period, ai_chat_credits_day
              * Required
          
        Returns:
            int
        """
        return self._api.doRequest("GET", self.getBaseApiPath() + "/usage/%s" % (usage_type))

    def getUsageHistory(self, **options):
        """
        Retrieves the daily history of the usage count associated with a particular service plan
        limit.
        
        Telerivet stores a snapshot of each organization's usage once per
        day, shortly after midnight in the organization's time zone. For usage types that are
        counted per day (`external_messages_day`, `api_requests_day`, `service_invocations_day`, and
        `ai_chat_credits_day`), each entry contains the usage counted during that entire day. For
        all other usage types, each entry contains the usage count at the time the snapshot was
        recorded.
        
        The maximum supported date range is 500 days between start_date and
        end_date. If the requested date range includes the current time, the response will also
        include a final entry with `current: true` containing the live usage count computed at the
        time of the API request.
        
        Usage snapshots are only recorded while an organization is active,
        so an entry may not be available for every date in the requested range.
        
        Arguments:
              * Required
            
            - usage_type (string)
                * Usage type, corresponding to the keys in the `plan_limits` property returned by
                    [getBillingDetails](#Organization.getBillingDetails).
                * Allowed values: contacts, phones, active_services, users, stored_messages,
                    service_invocations_day, api_requests_day, projects, data_rows, script_module_mb,
                    stored_file_mb, custom_actions, groups, custom_contact_fields,
                    external_messages_day, external_messages_period, ai_chat_credits_day
                * Required
            
            - start_date (string)
                * Start date of usage history, in YYYY-MM-DD format (in the organization's time
                    zone)
                * Required
            
            - end_date (string)
                * End date of usage history (inclusive), in YYYY-MM-DD format (in the organization's
                    time zone)
                * Required
          
        Returns:
            (associative array)
              - timezone_id (string)
                  * The organization's time zone ID, used to determine the date associated with each
                      entry
              
              - usage_type (string)
                  * The usage type from the request
              
              - history (array)
                  * List of usage entries in chronological order, one for each daily usage snapshot
                      recorded within the requested date range (plus the live usage entry if the range
                      includes the current time).
        """
        data = self._api.doRequest("GET", self.getBaseApiPath() + "/usage_history", options)
        return data

    def getMessageStats(self, **options):
        """
        Retrieves statistics about messages sent or received via Telerivet. This endpoint returns
        historical data that is computed shortly after midnight each day in the project's time zone,
        and does not contain message statistics for the current day.
        
        Arguments:
              * Required
            
            - start_date (string)
                * Start date of message statistics, in YYYY-MM-DD format
                * Required
            
            - end_date (string)
                * End date of message statistics (inclusive), in YYYY-MM-DD format
                * Required
            
            - rollup (string)
                * Date interval to group by
                * Allowed values: day, week, month, year, all
                * Default: day
            
            - properties (string)
                * Comma separated list of properties to group by
                * Allowed values: org_id, org_name, org_industry, project_id, project_name, user_id,
                    user_email, user_name, phone_id, phone_name, phone_type, direction, source, status,
                    network_code, network_name, message_type, service_id, service_name, simulated, link
            
            - metrics (string)
                * Comma separated list of metrics to return (summed for each distinct value of the
                    requested properties). Supported metrics are `count` (the number of messages),
                    `num_parts` (the number of SMS parts), `duration` (the total duration of calls, in
                    seconds), and `price.<currency>` (the total price of messages priced in the
                    specified ISO 4217 currency, e.g. `price.USD`). Amounts are not converted between
                    currencies: each `price.<currency>` metric only includes messages priced in the
                    specified currency.
                * Required
            
            - filters (dict)
                * Key-value pairs of properties and corresponding values; the returned statistics
                    will only include messages where the property matches the provided value. Only the
                    following properties are supported for filters: `user_id`, `phone_id`, `direction`,
                    `source`, `status`, `service_id`, `simulated`, `message_type`, `network_code`
          
        Returns:
            (associative array)
              - intervals (array)
                  * List of objects representing each date interval containing at least one message
                      matching the filters.
        """
        data = self._api.doRequest("GET", self.getBaseApiPath() + "/message_stats", options)
        return data

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
