package com.storage.cameras.rest.resource;

import com.storage.cameras.model.Keyword;
import java.util.List;
import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class CameraResource {

    private Long cameraId;

    private String rtspUrl;

    private List<CommentResource> comments;

    private String creationTimestamp;

    private String lastUpdateTimestamp;

    private String status;

    private String countryName;

    private String countryCode;

    private String city;

    private Set<Keyword> keywords;

    private String base64ImageData;

    private Set<LabelResource> labels;
}
