import gphotos
import instagram

filename = gphotos.download()
ret = instagram.upload(filename)

