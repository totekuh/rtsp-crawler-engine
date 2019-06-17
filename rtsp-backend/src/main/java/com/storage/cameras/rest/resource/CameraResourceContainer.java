package com.storage.cameras.rest.resource;

import lombok.Getter;

import java.util.List;

import static java.util.Collections.emptyList;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;

@Getter
public class CameraResourceContainer {
    private final int totalCount;
    private final List<CameraResource> cameras;

    public CameraResourceContainer(final List<CameraResource> cameras) {
        this.cameras = isNotEmpty(cameras) ? cameras : emptyList();
        this.totalCount = isNotEmpty(cameras) ? cameras.size() : 0;
    }
}
