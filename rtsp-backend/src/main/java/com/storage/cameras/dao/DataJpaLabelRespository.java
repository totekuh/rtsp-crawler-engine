package com.storage.cameras.dao;

import com.storage.cameras.model.Label;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DataJpaLabelRespository extends JpaRepository<Label, Long> {
    Label findByName(String name);
}
