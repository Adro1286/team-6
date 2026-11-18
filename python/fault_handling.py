from dataclasses import dataclass
from enum import IntEnum

class Severity(IntEnum):
    INFO = 0   #Non-critical events, used for logging
    WARNING = 1  #Minor anomalies, system can continue operating
    FAULT = 2  #Component-level failure
    CRITICAL = 3  #System-wide failure risk, requires immediate termination


class FaultCode:
    FLOW_SENSOR_INVALID = "FLOW_SENSOR_INVALID"
    RFID_READ_FAILED = "RFID_READ_FAILED"
    PROBE_POSITION_TIMEOUT = "PROBE_POSITION_TIMEOUT"
    TANK_LEVEL_HIGH = "TANK_LEVEL_HIGH"
    CLOUD_CONNECTION_LOST = "CLOUD_CONNECTION_LOST"
    EVENT_UPLOAD_FAILED = "EVENT_UPLOAD_FAILED"
    UNKNOWN_FAULT = "UNKNOWN_FAULT"

def get_fault_code(data: dict):
    if data.get("sensor_type") == "RFID" and data.get("device_status") == "FAULT":
        return FaultCode.RFID_READ_FAILED

    if (data.get("acknowledgment_status") in ["failure", "rejected"] 
        or data.get("connectivity_status") == "offline" 
        or data.get("authorization_status") == "unauthorized"
        or (data.get("transmission_retry_count", 0) >= data.get("max_retries", 3) and data.get("buffer_status") != "sent")
    ):
        return FaultCode.EVENT_UPLOAD_FAILED
    return FaultCode.UNKNOWN_FAULT

@dataclass
class Fault:
    fault_id: str
    fault_code: str
    severity: int
    severity_name: str
    fault_source: str

    station_id: str
    device_id: str
    sensor_type: str

    current_state: str
    device_status: str

    timestamp: str
    message: str
    recommended_action: str

    retry_count: int
    max_retries: int
    retry_status: str


class FaultException(Exception):

    def __init__(self, fault):
        self.fault = fault

        super().__init__(
            f"{fault.fault_code}: {fault.message}"
        )
