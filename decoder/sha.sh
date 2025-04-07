# cd C:/Users/aaron/Documents/charity/FIU-ectf25/decoder
docker build -t decoder .                                                                                                           
docker run --rm -v .\build_out:/out -v .\:/decoder -v .\..\secrets:/secrets -e DECODER_ID=0xdeadbeef decoder  