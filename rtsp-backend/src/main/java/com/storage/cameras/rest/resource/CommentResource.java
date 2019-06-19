package com.storage.cameras.rest.resource;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class CommentResource {
    private final String creationDate;
    private final String comment;
}
