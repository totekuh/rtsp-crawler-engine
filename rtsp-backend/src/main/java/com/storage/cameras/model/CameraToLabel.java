package com.storage.cameras.model;

import javax.persistence.Entity;
import static javax.persistence.FetchType.EAGER;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name = "camera_to_label")
public class CameraToLabel {

    private Long id;

    @ManyToOne(fetch = EAGER)
    @JoinColumn(name = "camera_id")
    private Camera camera;

    @ManyToOne(fetch = EAGER)
    @JoinColumn(name = "label_id")
    private Label label;
}
