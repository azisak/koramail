package yesa.student.koramail.fragments;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import butterknife.BindView;
import butterknife.ButterKnife;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import yesa.student.koramail.R;
import yesa.student.koramail.models.Key;
import yesa.student.koramail.networks.APIServices;
import yesa.student.koramail.networks.RetrofitInstance;
import yesa.student.koramail.utils.Globals;


public class KeyFragment extends Fragment {

    @BindView(R.id.container_content_private_key)
    TextView containerPrivateKey;
    @BindView(R.id.container_content_public_key)
    TextView containerPublicKey;
    @BindView(R.id.button_get_key)
    Button buttonGetKey;

    private APIServices apiServices;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_key, container, false);
        ButterKnife.bind(this, view);

        apiServices = RetrofitInstance.getInstance().create(APIServices.class);
        setOnClickListeners();

        return view;
    }

    private void setOnClickListeners() {
        View.OnClickListener onClickListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getKey();
            }
        };
        buttonGetKey.setOnClickListener(onClickListener);
    }

    private void getKey() {
        final ProgressDialog progressDialog = new ProgressDialog(getContext());
        progressDialog.setMessage(getResources().getString(R.string.message_loading));
        progressDialog.show();

        Call<Key> get = apiServices.getKey("yesasurya01@gmail.com");
        get.enqueue(new Callback<Key>() {
            @Override
            public void onResponse(Call<Key> call, Response<Key> response) {
                progressDialog.dismiss();
                Key key = response.body();
                if (key == null) return;

                Globals.DATA_PRIVATE_KEY = key.getPrivateKey();
                Globals.DATA_PUBLIC_KEY = key.getPublicKey();
                containerPrivateKey.setText(Globals.DATA_PRIVATE_KEY);
                containerPublicKey.setText(Globals.DATA_PUBLIC_KEY);
            }

            @Override
            public void onFailure(Call<Key> call, Throwable t) {
                progressDialog.dismiss();
                Toast.makeText(getContext(), t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
