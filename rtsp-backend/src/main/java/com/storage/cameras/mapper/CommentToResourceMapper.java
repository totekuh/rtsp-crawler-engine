package com.storage.cameras.mapper;

import com.storage.cameras.model.Comment;
import com.storage.cameras.rest.resource.CommentResource;

import static com.storage.cameras.util.DateTimeUtil.formatDateToString;

public interface CommentToResourceMapper {
    CommentToResourceMapper INSTANCE = comment -> new CommentResource(formatDateToString(comment.getCreationDate()),
            comment.getComment());

    CommentResource convert(Comment comment);
}
