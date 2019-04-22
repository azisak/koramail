package yesa.student.koramail.networks;

import java.util.List;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Path;
import yesa.student.koramail.models.DecryptedMail;
import yesa.student.koramail.models.EncryptedMail;
import yesa.student.koramail.models.Key;
import yesa.student.koramail.models.Mail;
import yesa.student.koramail.models.SignedMail;
import yesa.student.koramail.models.VerificationStatus;

public interface APIServices {
    @GET(Endpoints.URL_GET_KEY)
    Call<Key> getKey(@Path("email") String email);

    @POST(Endpoints.URL_ENCRYPT)
    @FormUrlEncoded
    Call<EncryptedMail> encrypt(
            @Field("message") String message,
            @Field("key") String key
    );

    @POST(Endpoints.URL_DECRYPT)
    @FormUrlEncoded
    Call<DecryptedMail> decrypt(
            @Field("message") String message,
            @Field("key") String key
    );

    @POST(Endpoints.URL_VERIFY)
    @FormUrlEncoded
    Call<VerificationStatus> verify(
            @Field("message") String message,
            @Field("public_key") String publicKey,
            @Field("signature") String signature
    );

    @POST(Endpoints.URL_SIGN)
    @FormUrlEncoded
    Call<SignedMail> sign(
            @Field("message") String message,
            @Field("private_key") String privateKey
    );

    @Multipart
    @POST(Endpoints.URL_SEND_MAIL)
    Call<Object> sendMail(
            @Path("email") String email,
            @Part("subject") RequestBody subject,
            @Part("receiver_mail") RequestBody receiver_mail,
            @Part("content") RequestBody content,
            @Part MultipartBody.Part attachment
    );

    @GET(Endpoints.URL_SEND_MAIL)
    Call<List<Mail>> getSentMails(@Path("email") String email);

    @GET(Endpoints.URL_INBOX)
    Call<List<Mail>> getInbox(@Path("email") String email);
}
