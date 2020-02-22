package com.storage.cameras.service;

import com.storage.cameras.dao.LabelDao;
import com.storage.cameras.model.Label;
import com.storage.cameras.rest.params.LabelParams;
import static java.util.Optional.ofNullable;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import static org.springframework.transaction.annotation.Propagation.REQUIRED;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
@Transactional(propagation = REQUIRED)
@AllArgsConstructor
public class LabelServiceImpl implements LabelService {
    private final LabelDao labelDao;

    @Override
    public Label findOrCreateLabel(LabelParams labelParams) {
        final String labelName = labelParams.getName();
        return ofNullable(labelDao.findByName(labelName))
                .orElseGet(() -> {
                    final Label newLabel = new Label();
                    newLabel.setName(labelName);
                    return newLabel;
                });
    }

    @Override
    public void save(Label label) {
        labelDao.save(label);
    }
}
