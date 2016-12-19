
from .entity import Entity

class MobileMoneyReceipt(Entity):
    """
    Represents a receipt received from a mobile money system such as Safaricom M-Pesa (Kenya),
    Vodacom M-Pesa (Tanzania), or Tigo Pesa (Tanzania).
    
    When your Android phone receives a SMS receipt from a supported mobile money
    service that Telerivet can understand, Telerivet will automatically parse it and create a
    MobileMoneyReceipt object.
    
    Fields:
    
      - id (string, max 34 characters)
          * Telerivet's internal ID for the receipt
          * Read-only
      
      - tx_id
          * Transaction ID from the receipt
          * Read-only
      
      - tx_type
          * Type of mobile money transaction
          * Allowed values: receive_money, send_money, pay_bill, deposit, withdrawal,
              airtime_purchase, balance_inquiry, reversal
          * Read-only
      
      - currency
          * [ISO 4217 Currency code](http://en.wikipedia.org/wiki/ISO_4217) for the transaction,
              e.g. KES or TZS. Amount, balance, and fee are expressed in units of this currency.
          * Read-only
      
      - amount (number)
          * Amount of this transaction; positive numbers indicate money added to your account,
              negative numbers indicate money removed from your account
          * Read-only
      
      - balance (number)
          * The current balance of your mobile money account (null if not available)
          * Read-only
      
      - fee (number)
          * The transaction fee charged by the mobile money system (null if not available)
          * Read-only
      
      - name
          * The name of the other person in the transaction (null if not available)
          * Read-only
      
      - phone_number
          * The phone number of the other person in the transaction (null if not available)
          * Read-only
      
      - time_created (UNIX timestamp)
          * The time this receipt was created in Telerivet
          * Read-only
      
      - other_tx_id
          * The other transaction ID listed in the receipt (e.g. the transaction ID for a
              reversed transaction)
          * Read-only
      
      - content
          * The raw content of the mobile money receipt
          * Read-only
      
      - provider_id
          * Telerivet's internal ID for the mobile money provider
          * Read-only
      
      - vars (dict)
          * Custom variables stored for this mobile money receipt
          * Updatable via API
      
      - contact_id
          * ID of the contact associated with the name/phone number on the receipt. Note that
              some mobile money systems do not provide the other person's phone number, so it's
              possible Telerivet may not automatically assign a contact_id, or may assign it to a
              different contact with the same name.
          * Updatable via API
      
      - phone_id
          * ID of the phone that received the receipt
          * Read-only
      
      - message_id
          * ID of the message corresponding to the receipt
          * Read-only
      
      - project_id
          * ID of the project this receipt belongs to
          * Read-only
    """

    def save(self):
        """
        Saves any fields or custom variables that have changed for this mobile money receipt.
        """
        super(MobileMoneyReceipt, self).save()

    def delete(self):
        """
        Deletes this receipt.
        """
        self._api.doRequest("DELETE", self.getBaseApiPath())

    def getBaseApiPath(self):
        return "/projects/%(project_id)s/receipts/%(id)s" % {'project_id': self.project_id, 'id': self.id} 
