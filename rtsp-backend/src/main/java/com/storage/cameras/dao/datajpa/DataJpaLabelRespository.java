package com.storage.cameras.dao.datajpa;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.Label;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface DataJpaLabelRespository extends JpaRepository<Label, Long> {
    Label findByName(String name);

    @Query(nativeQuery = true, value = "SELECT * FROM label l" +
            "WHERE EXISTS (SELECT 1 FROM camera_to_label ctl WHERE ctl.label_id = l.id AND ctl.camera_id =:cameraId)")
    List<Label> findAllByCameraId(Long cameraId);
}
