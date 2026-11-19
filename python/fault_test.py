from fault_handling import get_fault_code, FaultCode

def test_rfid_fail():
  data = {
    "sensor_type": "RFID",
    "device_status": "FAULT"
  }

  result = get_fault_code(data)
  print("Test Result #1: ", result)
  assert result == FaultCode.RFID_READ_FAILED

def test_event_upload_fail():
  data = {
    "station_id": "ST-001",
    "event_id": "EV-001",
    "connectivity_status": "online",
    "authorization_status": "authorized",
    "acknowledgment_status": "failure",
    "transmission_retry_count": 3,
    "max_retries": 3,
    "buffer_status": "pending",
    "error_code": "UPLOAD_TIMEOUT",
    "error_message": "cloud acknowledgment timed out"
  }

  result = get_fault_code(data)
  print("Test Result #2: ", result)
  assert result == FaultCode.EVENT_UPLOAD_FAILED

def test_successful_upload():
  data = {
    "connectivity_status": "online",
    "authorization_status": "authorized",
    "acknowledgment_status": "acepted",
    "transmission_retry_count": 0,
    "max_retries": 3,
    "buffer_status": "sent",
  }

  result = get_fault_code(data)
  print("Test Result #3: ", result)
  assert result == FaultCode.UNKNOWN_FAULT
    
