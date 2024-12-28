# Meetic
This project automates Microsoft Teams meeting analysis by extracting meeting recordings and data, generating summaries for each participant, identifying assigned tasks, and automatically sending personalized email follow-ups to attendees with their action items and meeting highlights.



سأقدم لك الخطوات بطريقة منظمة لإضافة الصلاحيات (Permissions) في Azure Portal:

1. **الدخول إلى Azure Portal**
   - افتح المتصفح واذهب إلى portal.azure.com
   - قم بتسجيل الدخول بحساب Azure الخاص بك

2. **الوصول إلى Azure Active Directory**
   - في الصفحة الرئيسية، ابحث عن "Azure Active Directory"
   - اضغط عليه للدخول إلى إعدادات Active Directory

3. **الذهاب إلى App registrations**
   - في القائمة اليسرى، اضغط على "App registrations"
   - ابحث عن تطبيقك (App ID: c3**************************3d5a)
   - اضغط على اسم التطبيق للدخول إلى إعداداته

4. **إضافة API Permissions**
   - في القائمة اليسرى للتطبيق، اضغط على "API permissions"
   - اضغط على زر "Add a permission"
   - اختر "Microsoft Graph" من القائمة

5. **اختيار نوع الصلاحيات**
   - اختر "Application permissions" (وليس Delegated)
   - هذا مهم جداً لأننا نستخدم Client Credentials Flow

6. **إضافة الصلاحيات المطلوبة**
   - ابحث وأضف الصلاحيات التالية:
     * `User.Read.All` (للوصول لمعلومات المستخدمين)
     * `Mail.Read` (لقراءة البريد)
     * `Mail.Send` (لإرسال البريد)
     * `CallRecords.Read.All` (لسجلات مكالمات Teams)

7. **منح موافقة المسؤول (Admin Consent)**
   - بعد إضافة جميع الصلاحيات
   - اضغط على زر "Grant admin consent" في أعلى قائمة الصلاحيات
   - أكد الموافقة في النافذة المنبثقة

8. **التحقق من الصلاحيات**
   - تأكد من أن جميع الصلاحيات تظهر علامة خضراء ✓
   - يجب أن تظهر عبارة "Granted for..." لكل صلاحية

9. **تحديث التطبيق**
   - يمكنك الآن العودة إلى التطبيق وتشغيله
   - يجب أن يعمل الآن بالصلاحيات الجديدة

ملاحظات مهمة:
- احرص على اختيار Application permissions وليس Delegated
- لا تنس أبداً خطوة "Grant admin consent"
- إذا لم تظهر بعض الصلاحيات، جرب البحث عنها باستخدام شريط البحث
- يمكنك حذف أي صلاحيات غير مستخدمة لتحسين الأمان

هل تريد مني توضيح أي خطوة من هذه الخطوات بشكل أكثر تفصيلاً؟