FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir -U pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

# Install Argos German->English model DURING BUILD 
RUN python -c "import argostranslate.package as p; p.update_package_index(); pkgs=p.get_available_packages(); pkg=next(x for x in pkgs if x.from_code=='de' and x.to_code=='en'); path=pkg.download(); p.install_from_path(path); print('Installed Argos de->en model from:', path)"

EXPOSE 8501

CMD ["streamlit", "run", "src/app_demo/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
