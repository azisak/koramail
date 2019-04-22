package yesa.student.koramail.activities;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;

import butterknife.BindView;
import butterknife.ButterKnife;

import java.util.Properties;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

import yesa.student.koramail.R;
import yesa.student.koramail.adapters.ViewPagerAdapter;
import yesa.student.koramail.fragments.InboxFragment;
import yesa.student.koramail.fragments.KeyFragment;
import yesa.student.koramail.fragments.NewMailFragment;
import yesa.student.koramail.fragments.SentMailFragment;
import yesa.student.koramail.utils.Preference;

public class MainActivity extends AppCompatActivity {

    @BindView(R.id.viewpager)
    ViewPager viewPager;
    @BindView(R.id.bottom_navigation_view)
    BottomNavigationView bottomNavigationView;

    private Preference preference;
    private static final String[] PERMISSIONSREQUIRED = {
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.INTERNET,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

        preference = new Preference(MainActivity.this);
        setupViewPager();
        setupBottomNavigationView();

        boolean allPermissionGranted = true;
        for (String permission : PERMISSIONSREQUIRED) {
            int grantResult = ContextCompat.checkSelfPermission(MainActivity.this, permission);
            if (grantResult == PackageManager.PERMISSION_DENIED) {
                allPermissionGranted = false;
                break;
            }
        }
        if (!allPermissionGranted) {
            ActivityCompat.requestPermissions(MainActivity.this, PERMISSIONSREQUIRED, 1);
        }
    }

    private void setupViewPager() {
        ViewPagerAdapter viewPagerAdapter = new ViewPagerAdapter(getSupportFragmentManager());
        viewPagerAdapter.addFragment(new InboxFragment(), getResources().getString(R.string.menu_inbox));
        viewPagerAdapter.addFragment(new SentMailFragment(), getResources().getString(R.string.menu_sent_mail));
        viewPagerAdapter.addFragment(new KeyFragment(), getResources().getString(R.string.menu_key));
        viewPagerAdapter.addFragment(new NewMailFragment(), getResources().getString(R.string.menu_create_mail));
        viewPager.setAdapter(viewPagerAdapter);
    }

    private void setupBottomNavigationView() {
        bottomNavigationView.setOnNavigationItemSelectedListener(
                new BottomNavigationView.OnNavigationItemSelectedListener() {
                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
                        if (menuItem.getItemId() == R.id.menu_inbox) {
                            viewPager.setCurrentItem(0);
                        } else if (menuItem.getItemId() == R.id.menu_sent_mail) {
                            viewPager.setCurrentItem(1);
                        } else if (menuItem.getItemId() == R.id.menu_key) {
                            viewPager.setCurrentItem(2);
                        } else if (menuItem.getItemId() == R.id.menu_create_mail) {
                            Intent newMail = new Intent(MainActivity.this, NewMailActivity.class);
                            startActivity(newMail);
                            return false;
                        } else if (menuItem.getItemId() == R.id.menu_logout) {
                            preference.removeEmail();
                            Intent signIn = new Intent(MainActivity.this, LoginActivity.class);
                            signIn.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK|Intent.FLAG_ACTIVITY_NEW_TASK);
                            startActivity(signIn);
                            return false;
                        }
                        return true;
                    }
                });
    }

    public void sendMail() {
        final String USERNAME = "yesasurya01@gmail.com";
        final String PASSWORD = "SVIzfehHfp2Fyqb9j3E5";

        final String DEST_USERNAME = "ysyesayesa@gmail.com";
        final String MAIL_SUBJECT = "Greeting!";
        final String MAIL_CONTENT = "Hello, World! from here, guys! Welcome to the world!";

        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.smtp.port", "587");

        Session session = Session.getInstance(
                props,
                new javax.mail.Authenticator() {
                    protected PasswordAuthentication getPasswordAuthentication() {
                        return new PasswordAuthentication(USERNAME, PASSWORD);
                    }
                });

        try {
            final Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(USERNAME));
            message.setRecipients(
                    Message.RecipientType.TO,
                    InternetAddress.parse(DEST_USERNAME)
            );
            message.setSubject(MAIL_SUBJECT);
            message.setText(MAIL_CONTENT);

            Thread thread = new Thread() {
                @Override
                public void run() {
                    super.run();
                    try {
                        Transport.send(message);
                    } catch (MessagingException e) {
                        e.printStackTrace();
                    }
                }
            };
            thread.start();

            System.out.println("EMAIL SENT...");
        } catch (MessagingException e) {
            throw new RuntimeException(e);
        }
    }
}