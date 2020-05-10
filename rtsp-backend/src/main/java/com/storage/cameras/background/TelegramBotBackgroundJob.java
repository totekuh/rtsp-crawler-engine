package com.storage.cameras.background;

import javax.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class TelegramBotBackgroundJob {
    @Value(value = "${TELEGRAM_BOT_TOKEN}")
    String botToken;

    @PostConstruct
    public void lookup() {
        final TelegramBotThread thread = new TelegramBotThread(botToken);
        new Thread(thread).start();
    }

    @AllArgsConstructor
    private static final class TelegramBotThread implements Runnable {
        private final String botToken;

        @Override
        public void run() {
            log.info("Activating the telegram C&C interface");
            while (true) {
                // FIXME: implement this
            }
        }
    }

}
