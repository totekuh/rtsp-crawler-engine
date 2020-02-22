package com.storage.cameras.rest.resource;

import java.util.List;
import lombok.Value;

@Value
public class CameraIdentifiersResource {
    List<Long> cameraIds; 
}
