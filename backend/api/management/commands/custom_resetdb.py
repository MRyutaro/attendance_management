from django.core.management.base import BaseCommand
from django.core.management import call_command
import sys


class Command(BaseCommand):
    help = "Reset the database and perform migrations"

    def confirm_reset(self):
        """
        ユーザに削除の確認を求めます。
        """
        confirm = input("Are you sure you want to reset the database? This action cannot be undone. (yes/no): ")
        return confirm.lower() == "yes"

    def handle(self, *args, **options):
        if not self.confirm_reset():
            self.stdout.write(self.style.NOTICE("Database reset aborted"))
            sys.exit()

        # データベースの削除
        call_command("flush", interactive=False, verbosity=0)

        # マイグレーションの実行
        call_command("makemigrations")
        self.stdout.write(self.style.SUCCESS("Migrations created successfully"))
        call_command("migrate")
        self.stdout.write(self.style.SUCCESS("Migrations completed successfully"))

        # スーパーユーザーの作成
        call_command("custom_createsuperuser")
        self.stdout.write(self.style.SUCCESS("Database reset and migrations completed successfully"))
