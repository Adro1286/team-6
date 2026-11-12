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


# test
test_fault = Fault(
    fault_id="FT-001",
    fault_code=FaultCode.RFID_READ_FAILED,
    severity=Severity.FAULT,
    severity_name="FAULT",
    fault_source="SENSOR",
    station_id="1234",
    device_id="5678",
    sensor_type="RFID",
    current_state="READING_RFID",
    device_status="FAULT",
    timestamp="2026-11-01T12:00:00Z",
    message="RFID read failed.",
    recommended_action="RETRY",
    retry_count=0,
    max_retries=3,
    retry_status="PENDING",
)

print(test_fault)

try:
    raise FaultException(test_fault)

except FaultException as error:
    print("\n")
    print("exception caught")
    print(error)