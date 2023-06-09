import os

from ...models import Company, CustomUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a new Superuser and Company based on the contents of the .env file"

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    def handle(self, *args, **options):
        # 会社情報を作成
        # .envファイルから会社情報を取得
        try:
            company_name = os.environ.get("DJANGO_SUPERCOMPANY_NAME")
            company_email = os.environ.get("DJANGO_SUPERCOMPANY_EMAIL")
            company_password = os.environ.get("DJANGO_SUPERCOMPANY_PASSWORD")
        except KeyError:
            self.stdout.write(
                self.style.ERROR("DJANGO_SUPER_COMPANYNAME, DJANGO_SUPER_COMPANYEMAIL, DJANGO_SUPER_COMPANYPASSWORD must be set in the .env file")
            )
            return

        if not company_name or not company_email or not company_password:
            self.stdout.write(
                self.style.ERROR("You must not set DJANGO_SUPER_COMPANYNAME, DJANGO_SUPER_COMPANYEMAIL, DJANGO_SUPER_COMPANYPASSWORD to empty in the .env file")
            )
            return

        company_email = self.normalize_email(company_email)

        # 会社情報を作成
        # もしすでにemailが存在していたら
        if not Company.objects.filter(email=company_email).exists():
            try:
                company = Company(
                    name=company_name, email=company_email, password=company_password
                )
                company.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create company: {e}"))
                return

        self.stdout.write(self.style.SUCCESS("Company created successfully"))

        # スーパーユーザーを作成
        # .envファイルからスーパーユーザー情報を取得
        try:
            superuser_name = os.environ.get("DJANGO_SUPERUSER_NAME")
            superuser_email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
            superuser_password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        except KeyError:
            self.stdout.write(
                self.style.ERROR("DJANGO_SUPER_USERNAME, DJANGO_SUPER_EMAIL, DJANGO_SUPER_PASSWORD must be set in the .env file")
            )
            return

        # 空白ならエラーをはく
        if not superuser_name or not superuser_email or not superuser_password:
            self.stdout.write(
                self.style.ERROR("You must not set DJANGO_SUPER_USERNAME, DJANGO_SUPER_EMAIL, DJANGO_SUPER_PASSWORD to empty in the .env file")
            )
            return

        # companyのidを取得
        try:
            company = Company.objects.get(email=company_email)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to get company: {e}"))
            return

        # スーパーユーザーを作成
        if not CustomUser.objects.filter(email=superuser_email).exists():
            try:
                superuser = CustomUser.objects.create_superuser(
                    company=company, name=superuser_name, email=superuser_email, password=superuser_password
                )
                superuser.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create superuser: {e}"))
                return

        self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
