package com.storage.cameras.model;

import static java.lang.Integer.parseInt;
import static java.lang.String.format;
import static java.util.Collections.emptySet;
import static java.util.stream.Collectors.toSet;
import static javax.persistence.EnumType.STRING;
import static javax.persistence.GenerationType.IDENTITY;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import static org.apache.commons.lang3.StringUtils.isBlank;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Arrays;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.OneToMany;
import javax.persistence.PrePersist;
import javax.persistence.PreUpdate;
import javax.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

@Getter
@Setter
@Entity
@Table(name = "camera")
@Slf4j
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

    @Column(name = "country_code", length = MAX_COUNTRY_CODE_LENGTH)
    private String countryCode;

    @Column(name = "country_name", length = MAX_COUNTRY_NAME_LENGTH)
    private String countryName;

    @Column(name = "isp", length = MAX_ISP_LENGTH)
    private String isp;

    @Column(name = "keywords")
    private String keywords;

    @OneToMany(mappedBy = "camera")
    private Set<Comment> comments = new HashSet<>();

    @Lob
    @Column(name = "base_64_image_data")
    private String base64ImageData;

    @PreUpdate
    public void updateTrigger() {
        this.updateTimestamp = new Date();
    }

    @PrePersist
    public void createTrigger() {
        this.updateTimestamp = new Date();
    }

    public Set<Keyword> getKeywords() {
        if (isBlank(keywords)) {
            return emptySet();
        }
        return Arrays.stream(keywords.split(","))
                .map(Keyword::valueOf)
                .collect(toSet());
    }

    public void addKeyword(final List<String> keywords) {
        if (isNotEmpty(keywords)) {
            for (final String k : keywords) {
                if (isBlank(this.keywords)) {
                    this.keywords = k;
                } else {
                    if (!this.keywords.contains(k)) {
                        this.keywords += format(",%s", k);
                    }
                }
            }
        }
    }

    public boolean isReachable() {
        try {
            final Socket socket = new Socket();
            socket.connect(new InetSocketAddress(getIpAddress(), getPort()), 5000);
            socket.close();
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    public String getIpAddress() {
        return url.split("rtsp://")[1].split(":")[0];
    }

    public int getPort() {
        return parseInt(url.split("rtsp://")[1].split(":")[1]);
    }
}
