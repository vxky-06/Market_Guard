def send_alert(transaction):
    """
    Sends an alert when a threat is detected. Currently prints to terminal.
    Args:
        transaction (dict): The transaction data that triggered the alert.
    """
    # For now, just print to terminal. This can be extended to send emails or Slack notifications.
    print(f"\033[91m[ALERT] Threat detected: {transaction}\033[0m") 