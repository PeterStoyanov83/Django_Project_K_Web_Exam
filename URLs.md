### Django URL Patterns and Views Mapping

---

#### Pages Views

- **Home**
    - URL: `/`
    - View: `pages.views.home`
    - Name: `pages:home`

- **About**
    - URL: `/about/`
    - View: `pages.views.about`
    - Name: `pages:about`

- **Contact**
    - URL: `/contact/`
    - View: `pages.views.contact`
    - Name: `pages:contact`

---

#### Admin Views

- **Main Admin Panel**
    - URL: `/admin/`
    - View: `django.contrib.admin.sites.index`
    - Name: `admin:index`

- **App-Specific Admin**
    - URL: `/admin/<app_label>/`
    - View: `django.contrib.admin.sites.app_index`
    - Name: `admin:app_list`

- **Authentication and Password Management**
    - URL: `/admin/login/`
        - View: `django.contrib.admin.sites.login`
        - Name: `admin:login`
    - URL: `/admin/logout/`
        - View: `django.contrib.admin.sites.logout`
        - Name: `admin:logout`
    - URL: `/admin/password_change/`
        - View: `django.contrib.admin.sites.password_change`
        - Name: `admin:password_change`
    - URL: `/admin/password_change/done/`
        - View: `django.contrib.admin.sites.password_change_done`
        - Name: `admin:password_change_done`

- **Autocomplete**
    - URL: `/admin/autocomplete/`
        - View: `django.contrib.admin.sites.autocomplete_view`
        - Name: `admin:autocomplete`

- **Admin JavaScript i18n**
    - URL: `/admin/jsi18n/`
        - View: `django.contrib.admin.sites.i18n_javascript`
        - Name: `admin:jsi18n`

---

#### Client Management Views

- **Laptops**
    - List: `/client/laptops/`
        - View: `client_management.views.laptop_list`
        - Name: `client_management:laptop_list`
    - Create: `/client/laptops/create/`
        - View: `client_management.views.laptop_create`
        - Name: `client_management:laptop_create`
    - Update: `/client/laptops/<int:pk>/update/`
        - View: `client_management.views.laptop_update`
        - Name: `client_management:laptop_update`
    - Delete: `/client/laptops/<int:pk>/delete/`
        - View: `client_management.views.laptop_delete`
        - Name: `client_management:laptop_delete`

- **Authentication**
    - Login: `/client/login/`
        - View: `client_management.views.user_login`
        - Name: `client_management:login`
    - Logout: `/client/logout/`
        - View: `client_management.views.user_logout`
        - Name: `client_management:logout`

- **Profiles**
    - Profile: `/client/profile/`
        - View: `client_management.views.profile`
        - Name: `client_management:profile`
    - Edit Profile: `/client/profile/edit/`
        - View: `client_management.views.profile_edit`
        - Name: `client_management:profile_edit`
    - Upload File: `/client/profile/upload-file/`
        - View: `client_management.views.upload_file`
        - Name: `client_management:upload_file`
    - Delete File: `/client/profile/delete-file/<int:file_id>/`
        - View: `client_management.views.delete_file`
        - Name: `client_management:delete_file`

- **Password Reset**
    - Reset: `/client/password_reset/`
        - View: `client_management.views.CustomPasswordResetView`
        - Name: `client_management:password_reset`
    - Reset Done: `/client/password_reset/done/`
        - View: `django.contrib.auth.views.PasswordResetDoneView`
        - Name: `client_management:password_reset_done`
    - Confirm Reset: `/client/reset/<uidb64>/<token>/`
        - View: `django.contrib.auth.views.PasswordResetConfirmView`
        - Name: `client_management:password_reset_confirm`
    - Reset Complete: `/client/reset/done/`
        - View: `django.contrib.auth.views.PasswordResetCompleteView`
        - Name: `client_management:password_reset_complete`

- **Registration**
    - Register: `/client/register/`
        - View: `client_management.views.register`
        - Name: `client_management:register`

---

#### Course Management Views

- **Courses**
    - List: `/course/`
        - View: `course_management.views.course_list`
        - Name: `course_management:course_list`
    - Detail: `/course/<int:pk>/`
        - View: `course_management.views.course_detail`
        - Name: `course_management:course_detail`
    - Create: `/course/create/`
        - View: `course_management.views.course_create`
        - Name: `course_management:course_create`
    - Update: `/course/<int:pk>/update/`
        - View: `course_management.views.course_update`
        - Name: `course_management:course_update`
    - Delete: `/course/<int:pk>/delete/`
        - View: `course_management.views.course_delete`
        - Name: `course_management:course_delete`

- **Applications**
    - Apply for Course: `/course/<int:course_id>/apply/`
        - View: `course_management.views.apply_for_course`
        - Name: `course_management:apply_for_course`
    - Approve Application: `/course/approve-application/<int:application_id>/`
        - View: `course_management.views.approve_course_application`
        - Name: `course_management:approve_course_application`
    - Reject Application: `/course/reject-application/<int:application_id>/`
        - View: `course_management.views.reject_course_application`
        - Name: `course_management:reject_course_application`

- **Schedules**
    - Create: `/course/<int:course_pk>/schedule/create/`
        - View: `course_management.views.schedule_create`
        - Name: `course_management:schedule_create`
    - Update: `/course/schedules/<int:pk>/update/`
        - View: `course_management.views.schedule_update`
        - Name: `course_management:schedule_update`
    - Delete: `/course/schedules/<int:pk>/delete/`
        - View: `course_management.views.schedule_delete`
        - Name: `course_management:schedule_delete`

- **Admin Panel**
    - Admin Courses: `/course/admin/courses/`
        - View: `course_management.views.admin_courses`
        - Name: `course_management:admin_courses`
    - Admin Lecturers: `/course/admin/lecturers/`
        - View: `course_management.views.admin_lecturers`
        - Name: `course_management:admin_lecturers`
    - Admin Users: `/course/admin/users/`
        - View: `course_management.views.admin_users`
        - Name: `course_management:admin_users`

---

#### API Views

- **Chat**
    - URL: `/api/chat/`
    - View: `api.openai_assistant.chat_with_assistant`
    - Name: `chat_with_assistant`
