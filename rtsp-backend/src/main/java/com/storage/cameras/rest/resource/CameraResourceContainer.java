package com.storage.cameras.rest.resource;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class CameraResourceContainer {
    private final Integer totalCount;
    private final List<CameraResource> cameras;

}
