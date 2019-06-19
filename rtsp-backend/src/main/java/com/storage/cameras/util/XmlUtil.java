package com.storage.cameras.util;

import lombok.NoArgsConstructor;
import static java.lang.String.format;
import static lombok.AccessLevel.PRIVATE;
import static org.apache.commons.lang3.StringUtils.isNotBlank;

@NoArgsConstructor(access = PRIVATE)
public final class XmlUtil {
    public static String extractTag(final String xml, final String tag) {
        if (isNotBlank(xml) && isNotBlank(tag)) {
            if (xml.contains(tag)) {
                return xml.split(format("<%s>", tag))[1].split(format("</%s>", tag))[0];
            } else {
                throw new IllegalStateException(
                        format("XML does not contain %s tag, XML: %s", tag, xml));
            }
        }
        throw new IllegalArgumentException("Parameters cannot be blank");
    }

}
