package yesa.student.koramail.activities;

import android.app.ProgressDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import butterknife.BindView;
import butterknife.ButterKnife;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import yesa.student.koramail.R;
import yesa.student.koramail.models.DecryptedMail;
import yesa.student.koramail.models.Key;
import yesa.student.koramail.models.VerificationStatus;
import yesa.student.koramail.networks.APIServices;
import yesa.student.koramail.networks.RetrofitInstance;
import yesa.student.koramail.utils.Globals;
import yesa.student.koramail.utils.Helpers;

public class ViewMailActivity extends AppCompatActivity {

    @BindView(R.id.container_title_email)
    TextView containerTitleEmail;
    @BindView(R.id.container_content_email)
    TextView containerContentEmail;
    @BindView(R.id.container_content_subject)
    TextView containerContentSubject;
    @BindView(R.id.container_content_content)
    TextView containerContentContent;
    @BindView(R.id.button_verify)
    Button buttonVerify;
    @BindView(R.id.button_decrypt)
    Button buttonDecrypt;
    @BindView(R.id.container_key)
    EditText containerKey;
    @BindView(R.id.container_title_attachment)
    TextView containerTitleAttachment;
    @BindView(R.id.container_content_attachment)
    TextView containerContentAttachment;

    private APIServices apiServices;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_mail);
        ButterKnife.bind(this);

        apiServices = RetrofitInstance.getInstance().create(APIServices.class);
        setOnClickListeners();

        containerContentSubject.setText(Globals.DATA_VIEWED_EMAIL.getSubject());
        containerContentEmail.setText(Globals.DATA_VIEWED_EMAIL.getSender());
        containerContentContent.setText(Globals.DATA_VIEWED_EMAIL.getContent());
        if (Globals.DATA_VIEWED_EMAIL.getAttachmentPaths() != null && !Globals.DATA_VIEWED_EMAIL.getAttachmentPaths().isEmpty() ) {
            containerTitleAttachment.setVisibility(View.VISIBLE);
            containerContentAttachment.setVisibility(View.VISIBLE);
            String[] names = Globals.DATA_VIEWED_EMAIL.getAttachmentPaths().get(0).split("/");
            String name = names[names.length - 1];
            containerContentAttachment.setText(name);

            View.OnClickListener onClickListener = new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String address = "http://35.240.202.170:5000" + Globals.DATA_VIEWED_EMAIL.getAttachmentPaths().get(0);
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    intent.setData(Uri.parse(address));
                    startActivity(intent);
                }
            };
            containerTitleAttachment.setOnClickListener(onClickListener);
            containerContentAttachment.setOnClickListener(onClickListener);
        }
    }

    private void setOnClickListeners() {
        View.OnClickListener onClickListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String content = containerContentContent.getText().toString();
                String key = containerKey.getText().toString();
                if (key.length() < 4) {
                    String message = "Key must be minimum length of 4.";
                    Helpers.showWarning(ViewMailActivity.this, message);
                } else {
                    decrypt(content, key);
                }
            }
        };
        buttonDecrypt.setOnClickListener(onClickListener);

        onClickListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                verify();
            }
        };
        buttonVerify.setOnClickListener(onClickListener);
    }

    private void decrypt(String message, String key) {
        final ProgressDialog progressDialog = new ProgressDialog(ViewMailActivity.this);
        progressDialog.setMessage(getResources().getString(R.string.message_loading));
        progressDialog.show();

        Call<DecryptedMail> post = apiServices.decrypt(message, key);
        post.enqueue(new Callback<DecryptedMail>() {
            @Override
            public void onResponse(Call<DecryptedMail> call, Response<DecryptedMail> response) {
                progressDialog.dismiss();
                DecryptedMail mail = response.body();
                if (mail == null) return;

                containerContentContent.setText(mail.getDecryptedMessage());
                buttonVerify.setEnabled(false);
                buttonDecrypt.setEnabled(false);
                containerKey.setEnabled(false);
            }

            @Override
            public void onFailure(Call<DecryptedMail> call, Throwable t) {
                progressDialog.dismiss();
                Toast.makeText(ViewMailActivity.this, t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void verify() {
        final ProgressDialog progressDialog = new ProgressDialog(ViewMailActivity.this);
        progressDialog.setMessage(getResources().getString(R.string.message_loading));
        progressDialog.show();

        Call<Key> get = apiServices.getKey(Globals.DATA_VIEWED_EMAIL.getSender());
        get.enqueue(new Callback<Key>() {
            @Override
            public void onResponse(Call<Key> call, Response<Key> response) {
                Key key = response.body();
                if (key == null) return;

                String message = Globals.DATA_VIEWED_EMAIL.getContent();
                String publicKey = key.getPublicKey();
                final String content = Helpers.getContentFromSignedContent(message);
                String signature = Helpers.getSignatureFromSignedContent(message);

                Call<VerificationStatus> post = apiServices.verify(content, publicKey, signature);
                post.enqueue(new Callback<VerificationStatus>() {
                    @Override
                    public void onResponse(Call<VerificationStatus> call,
                                           Response<VerificationStatus> response) {
                        progressDialog.dismiss();
                        VerificationStatus status = response.body();
                        if (status == null) return;

                        if (status.getVerified()) {
                            String message = "Verification Success.";
                            Helpers.showWarning(ViewMailActivity.this, message);
                        } else {
                            String message = "Verification Failed.";
                            Helpers.showWarning(ViewMailActivity.this, message);
                        }

                        containerContentContent.setText(content);
                        buttonVerify.setEnabled(false);
                    }

                    @Override
                    public void onFailure(Call<VerificationStatus> call, Throwable t) {
                        progressDialog.dismiss();
                        Toast.makeText(ViewMailActivity.this, t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
                    }
                });
            }

            @Override
            public void onFailure(Call<Key> call, Throwable t) {
                progressDialog.dismiss();
                Toast.makeText(ViewMailActivity.this, t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
