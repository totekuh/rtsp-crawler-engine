package com.storage.cameras.dao.datajpa;

import com.storage.cameras.model.Comment;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DataJpaCommentRepository extends JpaRepository<Comment, Long> {
}
