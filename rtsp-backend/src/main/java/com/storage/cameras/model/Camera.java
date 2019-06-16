package com.storage.cameras.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.Date;

import static javax.persistence.EnumType.STRING;
import static javax.persistence.GenerationType.IDENTITY;

@Getter
@Setter
@Entity
@Table(name = "camera")
public class Camera {
    public static final int MAX_COMMENT_LENGTH = 200;
    private static final int MAX_CAMERA_URL_LENGTH = 50;
    private static final int MAX_CITY_NAME_LENGTH = 255;
    private static final int MAX_COUNTRY_CODE_LENGTH = 10;
    private static final int MAX_COUNTRY_NAME_LENGTH = 50;
    private static final int MAX_STATUS_LENGTH = 50;
    private static final int MAX_ISP_LENGTH = 200;

    @Id
    @GeneratedValue(strategy = IDENTITY)
    private Long id;

    @Column(name = "creation_timestamp", nullable = false)
    private Date creationTimestamp;

    @Column(name = "update_timestamp", nullable = false)
    private Date updateTimestamp;

    @Column(name = "url", nullable = false, length = MAX_CAMERA_URL_LENGTH, unique = true)
    private String url;

    @Enumerated(STRING)
    @Column(name = "status", nullable = false, length = MAX_STATUS_LENGTH)
    private CameraStatus status;

    @Column(name = "city", length = MAX_CITY_NAME_LENGTH)
    private String city;

    @Column(name = "comment", length = MAX_COMMENT_LENGTH)
    private String comment;

    @Column(name = "country_code", length = MAX_COUNTRY_CODE_LENGTH)
    private String countryCode;

    @Column(name = "country_name", length = MAX_COUNTRY_NAME_LENGTH)
    private String countryName;

    @Column(name = "isp", length = MAX_ISP_LENGTH)
    private String isp;

    @PreUpdate
    public void updateTrigger() {
        this.updateTimestamp = new Date();
    }

    @PrePersist
    public void createTrigger() {
        this.updateTimestamp = new Date();
    }

    public boolean isNewlyCreated() {
        return id == null;
    }
}


