package com.storage.cameras.model;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;

import static javax.persistence.FetchType.EAGER;
import static javax.persistence.GenerationType.IDENTITY;

@Data
@Entity
@Table(name = "comment")
public class Comment {

    public static final int MAX_COMMENT_LENGTH = 255;
    @Id
    @GeneratedValue(strategy = IDENTITY)
    private Long id;

    @Column(name = "comment", length = MAX_COMMENT_LENGTH, nullable = false)
    private String comment;

    @Column(name = "creation_date", nullable = false)
    private Date creationDate = new Date();

    @ManyToOne(fetch = EAGER)
    @JoinColumn(name = "camera_id")
    private Camera camera;
}
