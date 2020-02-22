package com.storage.cameras.model;

import javax.persistence.Entity;
import static javax.persistence.FetchType.EAGER;
import javax.persistence.GeneratedValue;
import static javax.persistence.GenerationType.IDENTITY;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name = "camera_to_label")
public class CameraToLabel {
    @Id
    @GeneratedValue(strategy = IDENTITY)
    private Long id;

    @ManyToOne(fetch = EAGER)
    @JoinColumn(name = "camera_id")
    private Camera camera;

    @ManyToOne(fetch = EAGER)
    @JoinColumn(name = "label_id")
    private Label label;
}
