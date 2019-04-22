package yesa.student.koramail.models;

import com.google.gson.annotations.SerializedName;

public class Key {
    @SerializedName("public_key")
    private String publicKey;
    @SerializedName("private_key")
    private String privateKey;

    public String getPublicKey() {
        return publicKey;
    }

    public void setPublicKey(String publicKey) {
        this.publicKey = publicKey;
    }

    public String getPrivateKey() {
        return privateKey;
    }

    public void setPrivateKey(String privateKey) {
        this.privateKey = privateKey;
    }
}
