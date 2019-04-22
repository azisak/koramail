package yesa.student.koramail.activities;

import android.app.ProgressDialog;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.webkit.MimeTypeMap;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import butterknife.BindView;
import butterknife.ButterKnife;

import java.io.File;
import java.net.URI;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.regex.Matcher;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import yesa.student.koramail.R;
import yesa.student.koramail.models.EncryptedMail;
import yesa.student.koramail.models.SignedMail;
import yesa.student.koramail.networks.APIServices;
import yesa.student.koramail.networks.RetrofitInstance;
import yesa.student.koramail.utils.Globals;
import yesa.student.koramail.utils.Helpers;
import yesa.student.koramail.utils.Preference;


public class NewMailActivity extends AppCompatActivity {

    @BindView(R.id.container_email)
    EditText containerEmail;
    @BindView(R.id.container_subject)
    EditText containerSubject;
    @BindView(R.id.container_content)
    EditText containerContent;
    @BindView(R.id.switch_is_encrypted)
    Switch switchIsEncrypted;
    @BindView(R.id.container_key)
    EditText containerKey;
    @BindView(R.id.switch_is_with_signature)
    Switch switchIsWithSignature;
    @BindView(R.id.button_send_mail)
    Button buttonSendMail;
    @BindView(R.id.button_add_attachment)
    Button buttonAddAttachment;
    @BindView(R.id.container_attachment_name)
    TextView containerAttachmentName;

    private String email;
    private String subject;
    private String content;
    private String enryptedContent;
    private Boolean isEncrypted;
    private Boolean isWithSignature;
    private APIServices apiServices;
    private Preference preference;
    private int REQ_CODE_PICKFILE = 1;
    private File attachment = null;
    private Uri attachmentUri;
    private boolean isAttachmentAttached = false;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_mail);
        ButterKnife.bind(this);

        apiServices = RetrofitInstance.getInstance().create(APIServices.class);
        preference = new Preference(NewMailActivity.this);
        setOnClickListeners();
        setOnSwitchChangeListeners();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQ_CODE_PICKFILE) {
            if (resultCode == RESULT_OK) {
                String path = data.getData().getPath().split(":")[1];
                attachment = new File(Environment.getExternalStorageDirectory().getAbsolutePath(), path);

                isAttachmentAttached = true;
                containerAttachmentName.setVisibility(View.VISIBLE);
                containerAttachmentName.setText(attachment.getName());
                buttonAddAttachment.setText("Delete Attachment");
            }
        }
    }

    private void setOnClickListeners() {
        View.OnClickListener onClickListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (validateForm()) {
                    sendMail();
                }
            }
        };
        buttonSendMail.setOnClickListener(onClickListener);

        onClickListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!isAttachmentAttached) {
                    Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                    attachment = getTemporaryFile();
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                        attachmentUri = FileProvider.getUriForFile(NewMailActivity.this,
                                "yesa.student.koramail", attachment);
                    } else {
                        attachmentUri = Uri.fromFile(attachment);
                    }
                    intent.putExtra(MediaStore.EXTRA_OUTPUT, attachmentUri);
                    intent.setType("*/*");
                    startActivityForResult(intent, REQ_CODE_PICKFILE);
                } else {
                    isAttachmentAttached = false;
                    attachment = null;
                    containerAttachmentName.setVisibility(View.GONE);
                    buttonAddAttachment.setText("Add Attachment");
                }
            }
        };
        buttonAddAttachment.setOnClickListener(onClickListener);
    }

    private void setOnSwitchChangeListeners() {
        switchIsEncrypted.setOnCheckedChangeListener(
                new CompoundButton.OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        if (isChecked) {
                            String content = containerContent.getText().toString();
                            if (content.isEmpty()) {
                                switchIsEncrypted.setChecked(false);
                                String message = "Message cannot be empty!";
                                Helpers.showWarning(NewMailActivity.this, message);
                                return;
                            }
                            String key = containerKey.getText().toString();
                            if (key.length() < 4) {
                                switchIsEncrypted.setChecked(false);
                                String message = "Key must be minimum length of 4.";
                                Helpers.showWarning(NewMailActivity.this, message);
                            } else {
                                encrypt(content, key);
                            }
                        } else {
                            containerContent.setText(content);
                            containerKey.setText("");
                            containerKey.setEnabled(true);
                        }
                    }
                });

        switchIsWithSignature.setOnCheckedChangeListener(
                new CompoundButton.OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        String content = containerContent.getText().toString();
                        if (content.isEmpty()) {
                            switchIsWithSignature.setChecked(false);
                            String message = "Message cannot be empty!";
                            Helpers.showWarning(NewMailActivity.this, message);
                            return;
                        }
                        if (Globals.DATA_PRIVATE_KEY.isEmpty()) {
                            switchIsWithSignature.setChecked(false);
                            String message = "Please generate your key first!";
                            Helpers.showWarning(NewMailActivity.this, message);
                            return;
                        }
                        containerContent.setEnabled(false);
                        switchIsEncrypted.setEnabled(false);
                        containerKey.setEnabled(false);
                        switchIsWithSignature.setEnabled(false);
                        sign(content, Globals.DATA_PRIVATE_KEY);
                    }
                });
    }

    private void sendMail() {
        final ProgressDialog progressDialog = new ProgressDialog(NewMailActivity.this);
        progressDialog.setMessage(getResources().getString(R.string.message_loading));
        progressDialog.show();
        
        String email = containerEmail.getText().toString();
        String subject = containerSubject.getText().toString();
        String content = containerContent.getText().toString();

        RequestBody subjectBody = RequestBody.create(MediaType.parse("text/plain"), subject);
        RequestBody receiverMailBody = RequestBody.create(MediaType.parse("text/plain"), email);
        RequestBody contentBody = RequestBody.create(MediaType.parse("text/plain"), content);
        RequestBody attachmentBody = RequestBody.create(MediaType.parse("*/*"), attachment);
        MultipartBody.Part attachmentPart = MultipartBody.Part.createFormData("file", attachment.getName(), attachmentBody);

        Call<Object> post = apiServices.sendMail(preference.getEmail(), subjectBody, receiverMailBody, contentBody, attachmentPart);
        post.enqueue(new Callback<Object>() {
            @Override
            public void onResponse(Call<Object> call, Response<Object> response) {
                progressDialog.dismiss();
                String message = "Email has been sent.";
                Toast.makeText(NewMailActivity.this, message, Toast.LENGTH_SHORT).show();
                finish();
            }

            @Override
            public void onFailure(Call<Object> call, Throwable t) {
                progressDialog.dismiss();
                Toast.makeText(NewMailActivity.this, t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void encrypt(String _content, String key) {
        final ProgressDialog progressDialog = new ProgressDialog(NewMailActivity.this);
        progressDialog.setMessage(getResources().getString(R.string.message_loading));
        progressDialog.show();

        Call<EncryptedMail> post = apiServices.encrypt(_content, key);
        post.enqueue(new Callback<EncryptedMail>() {
            @Override
            public void onResponse(Call<EncryptedMail> call, Response<EncryptedMail> response) {
                progressDialog.dismiss();
                EncryptedMail mail = response.body();
                if (mail == null) return;

                content = containerContent.getText().toString();
                enryptedContent = mail.getEncryptedMessage();
                containerContent.setText(enryptedContent);
                containerKey.setEnabled(false);
            }

            @Override
            public void onFailure(Call<EncryptedMail> call, Throwable t) {
                progressDialog.dismiss();
                Toast.makeText(NewMailActivity.this, t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void sign(String message, String key) {
        final ProgressDialog progressDialog = new ProgressDialog(NewMailActivity.this);
        progressDialog.setMessage(getResources().getString(R.string.message_loading));
        progressDialog.show();

        Call<SignedMail> post = apiServices.sign(message, key);
        post.enqueue(new Callback<SignedMail>() {
            @Override
            public void onResponse(Call<SignedMail> call, Response<SignedMail> response) {
                progressDialog.dismiss();
                SignedMail mail = response.body();
                if (mail == null) return;

                String signedContent = Helpers.generateSignedContent(mail.getMessage(), mail.getSignature());
                containerContent.setText(signedContent);
            }

            @Override
            public void onFailure(Call<SignedMail> call, Throwable t) {
                progressDialog.dismiss();
                Toast.makeText(NewMailActivity.this, t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private Boolean validateForm() {
        email = containerEmail.getText().toString();
        subject = containerSubject.getText().toString();
        content = containerContent.getText().toString();
        isEncrypted = switchIsEncrypted.isActivated();
        isWithSignature = switchIsWithSignature.isActivated();

        if (email.isEmpty() || subject.isEmpty() || content.isEmpty()) {
            String message = "Please complete all the fields.";
            Helpers.showWarning(NewMailActivity.this, message);
            return false;
        }

        Matcher matcher = Globals.REGEX_EMAIL.matcher(email);
        if (!matcher.find()) {
            String message = "Email is not in correct form.";
            Helpers.showWarning(NewMailActivity.this, message);
            return false;
        }

        return true;
    }

    private String getRealPathFromURI(Uri contentURI) {
        String result;
        Cursor cursor = getContentResolver().query(contentURI, null, null, null, null);
        if (cursor == null) {
            result = contentURI.getPath();
        } else {
            cursor.moveToFirst();
//            int idx = cursor.getColumnIndex(MediaStore.Images.ImageColumns.DATA);
            result = cursor.getString(0);
            cursor.close();
        }
        return result;
    }

    public File getTemporaryFile() {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
        String fileName = "temp_" + timeStamp;
        return new File(Environment.getExternalStorageDirectory(), fileName);
    }
}
