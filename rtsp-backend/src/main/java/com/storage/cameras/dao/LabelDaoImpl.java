package com.storage.cameras.dao;

import com.storage.cameras.dao.datajpa.DataJpaLabelRespository;
import com.storage.cameras.model.Camera;
import com.storage.cameras.model.Label;
import static java.util.Collections.emptyList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import org.springframework.stereotype.Repository;

@Repository
@AllArgsConstructor
@Slf4j
public class LabelDaoImpl implements LabelDao {
    private final DataJpaLabelRespository dataJpaLabelRespository;

    @Override
    public Label findByName(String name) {
        return dataJpaLabelRespository.findByName(name);
    }

    @Override
    public Label save(Label label) {
        return dataJpaLabelRespository.save(label);
    }

    @Override
    public List<Label> findLabelsByCamera(Camera camera) {
        final List<Label> labels = dataJpaLabelRespository.findAllByCameraId(camera.getId());
        if (isNotEmpty(labels)) {
            return labels;
        }
        else {
            return emptyList();
        }
    }
}
