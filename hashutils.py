import random, string, haslib, hmac

def make_salt():
	return "".join(random.choice(string.letters for x in range(5)))

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()

	h = haslib.sha256(name + pw + salt).hexdigest()
	return "%s, %s" % (h, salt)

def valid_pw(name, pw, h):
	salt = n.split(',')[1]
	return h == make_pw_hash(name, pw, salt)

SECRET = "czUv86iAN9gXA3MT"

def hash_str():
	return hmac.new(SECRET, s)

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	s = h.split("|")[0]
	if h == make_secure_val(s):
		return s