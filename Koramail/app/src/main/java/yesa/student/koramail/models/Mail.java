package yesa.student.koramail.models;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class Mail {

    @SerializedName("id")
    private Integer id;
    @SerializedName("subject")
    private String subject;
    @SerializedName("sender_mail")
    private String sender;
    @SerializedName("receiver_mail")
    private String receiver;
    @SerializedName("content")
    private String content;
    @SerializedName("attachment_paths")
    private List<String> attachmentPaths;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public String getSender() {
        return sender;
    }

    public void setSender(String sender) {
        this.sender = sender;
    }

    public String getReceiver() {
        return receiver;
    }

    public void setReceiver(String receiver) {
        this.receiver = receiver;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public List<String> getAttachmentPaths() {
        return attachmentPaths;
    }

    public void setAttachmentPaths(List<String> attachmentPaths) {
        this.attachmentPaths = attachmentPaths;
    }
}