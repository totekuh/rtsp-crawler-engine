package com.storage.cameras.rest.params;

import lombok.Value;

@Value
public class ScanCameraParams {
    String ipAddress;
    int port;
}
