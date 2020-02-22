package com.storage.cameras.dao;

import com.storage.cameras.dao.datajpa.DataJpaLabelRespository;
import com.storage.cameras.model.Label;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
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
}
