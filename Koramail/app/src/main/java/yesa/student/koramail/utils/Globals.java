package yesa.student.koramail.utils;

import java.util.regex.Pattern;

import javax.mail.Session;

import yesa.student.koramail.models.Mail;

public class Globals {

    public final static String BASE_ENDPOINT_URL = "http://35.240.202.170:5000/api/";

    public final static String SMTP_AUTH_KEY = "mail.smtp.auth";
    public final static String SMTP_TLS_ENABLED_KEY = "mail.smtp.starttls.enable";
    public final static String SMTP_HOST_KEY = "mail.smtp.host";
    public final static String SMTP_PORT_KEY = "mail.smtp.port";

    public final static String SMTP_AUTH_VAL = "true";
    public final static String SMTP_TLS_ENABLED_VAL = "true";
    public final static String SMTP_HOST_VAL = "smtp.gmail.com";
    public final static String SMTP_PORT_VAL = "587";

    public static Session SESSION = null;

    public final static Pattern REGEX_EMAIL =
            Pattern.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}$", Pattern.CASE_INSENSITIVE);

    //IN-MEMORY DATA
    public static String DATA_PUBLIC_KEY = "";
    public static String DATA_PRIVATE_KEY = "";
    public static Mail DATA_VIEWED_EMAIL;
}
