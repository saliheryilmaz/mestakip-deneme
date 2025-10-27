# GitHub'a Yükleme Komutları

Terminal'de bir sorun olduğu için, lütfen aşağıdaki komutları sırasıyla çalıştırın:

## 1. Git Durumunu Kontrol Et
```bash
git status
```

## 2. Eğer Merge Process Devam Ediyorsa
```bash
git merge --abort
```

## 3. Değişiklikleri Pull Et
```bash
git pull origin main --rebase
```

VEYA merge isterseniz:
```bash
git pull origin main
```
(Eğer merge mesajı ister, `:wq` yazarak kaydedip çıkın - Vim kullanıyorsanız)

## 4. Ardından Push Yapın
```bash
git push origin main
```

## Alternatif Yöntem (Eğer Sorun Devam Ederse)

### Force Push (Dikkatli Kullanın!)
```bash
# Bu method yereldeki değişiklikleri zorla gönderir
git push origin main --force
```

**Not:** Force push yalnızca gerektiğinde kullanın. Başkalarıyla çalışıyorsanız güvenli değildir.

## Manuel Çözüm

Eğer yukarıdaki komutlar çalışmazsa:

1. **VS Code'dan Git Kurulumu:**
   - Ctrl+Shift+P
   - "Git: Publish Branch" yazın
   - "Push" seçeneğini seçin

2. **GitHub Desktop:**
   - GitHub Desktop uygulamasını kullanın
   - Commit mesajını yazın
   - "Push origin" butonuna tıklayın

3. **Manuel Kontrol:**
   - Değişikliklerinizi tek tek gözden geçirin
   - GitHub web arayüzünden repository'nizi kontrol edin
   - Gerekirse GitHub'dan güncellemeleri indirin

## Şu Anki Durum

✅ Değişiklikler commit edildi:
- metis_admin/settings.py
- Procfile
- nixpacks.toml
- .gitignore
- railway.json (silindi)
- RAILWAY_DEPLOY.md (yeni)
- RAILWAY_DEPLOY_SUMMARY.md (yeni)

⏳ Push işlemi bekliyor - remote ile conflict var

## Çözüm

En basit yöntem:
```bash
git pull origin main --rebase
git push origin main
```

Eğer bu da çalışmazsa, GitHub Desktop uygulaması kullanarak sorunsuz push edebilirsiniz.

