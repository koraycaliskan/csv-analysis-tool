import sys
import os
import streamlit.web.cli as stcli

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.abspath(os.path.join(sys._MEIPASS, path))
    return os.path.abspath(os.path.join(os.getcwd(), path))

if __name__ == "__main__":
    try:
        app_path = resolve_path("app.py")
        print(f"Uygulama Başlatılıyor: {app_path}")
        
        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--server.headless", "true",
            "--server.port", "8501",
            "--global.developmentMode", "false"
        ]
        sys.exit(stcli.main())
    except Exception as e:
        print(f"KRITIK HATA: {e}")
        import traceback
        traceback.print_exc()
        input("\nDevam etmek icin Enter'a basin...")