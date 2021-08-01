# Milking-Project
 🐄👉🥛 

Auto verify 6-digit code in CowTransfer, and show them in local website

## 📕 Manual

1. Download Python3.8 and pip
2. run `pip install -r requirements`
3. visit [cowtransfer.com](https://cowtransfer.com/), and [find your cookie](https://www.wikihow.com/View-Cookies)
4. Use your cookie to fill in the `cookie` variable in `milk/milk.py`
5. run `python3 app.py`
6. visit `localhost:5000/milk`, and you will see a form showing all the valid codes

An example of `cookie`:

```python
cookie = "cf-cs-k-20181214=160812367954593; \
        dont_show_gift_icon=true; \
        gr_user_id=43512091-4af4-4980-928c-3e277260dca2; \
        JSESSIONID=7031A02agwertf7B3AB11348B98A1;\
        SERVERID=b56eba7d58f8662502ef0667d2fc4489|1608290818|1608284650"
```

## ❗ Warning

&emsp;&emsp; The project is only used for learning.

## 🎯 Need to Do

- [ ] use NLP to separate spam files