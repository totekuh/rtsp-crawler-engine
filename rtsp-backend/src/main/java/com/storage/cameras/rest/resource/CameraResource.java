package com.storage.cameras.rest.resource;

import com.storage.cameras.model.Keyword;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.List;
import java.util.Set;

@Getter
@AllArgsConstructor
public class CameraResource {

    private final Long cameraId;

    private final String rtspUrl;

    private List<CommentResource> comments;

    private String creationTimestamp;

    private String lastUpdateTimestamp;

    private final String status;

    private final String countryName;

    private final String countryCode;

    private final String city;

    private Set<Keyword> keywords;

}
