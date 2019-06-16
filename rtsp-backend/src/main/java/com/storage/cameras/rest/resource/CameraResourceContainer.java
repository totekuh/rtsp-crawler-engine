package com.storage.cameras.rest.resource;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.List;

@Getter
@AllArgsConstructor
public class CameraResourceContainer {
    private final Integer totalCount;
    private final List<CameraResource> cameras;

}
