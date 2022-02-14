from collections import Counter
import re

import random
import itertools
from math import log

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def language_model(sentence, word_counter, bigram_counter, use_log=True):
    prob = 0 if use_log else 1.
    for bigram in zip(sentence, sentence[1:]):
        # TODO: To avoid vanishing probabilities, we should consider maximizing
        # the sum of the log-probabilities.
        # NOTE: If the word is not present in the dictionary, we assume a very
        # small probability of it appearing the translation.
        if word_counter[bigram[0]] == 0:
            if use_log:
                prob += 1e-32
            else:
                prob *= 1e-15
        else:
            p = bigram_counter[bigram] / word_counter[bigram[0]]
            if use_log:
                prob += log(p + 1e-32)
            else:
                prob *= p
    return prob

def main():
    sample_text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse eget facilisis elit. Interdum et malesuada fames ac ante ipsum primis in faucibus. Duis in ante egestas, elementum tortor at, dignissim odio. Phasellus sed volutpat neque. Quisque et efficitur tellus. Nulla at venenatis magna. Nunc porttitor at metus luctus dapibus. Maecenas volutpat mauris sit amet metus semper, a iaculis elit consequat. Quisque vulputate sagittis sem, a gravida orci porttitor vel. Nam justo eros, tincidunt id aliquet a, vulputate ac tortor. Vestibulum lobortis enim a varius rutrum. Phasellus aliquet tortor eros, a scelerisque ipsum bibendum at. Cras eget fermentum urna, sed dapibus arcu. Ut id nisl at velit ornare commodo. Vestibulum pellentesque, purus vel suscipit ornare, risus justo eleifend elit, nec dignissim eros metus vel elit.
Sed et arcu nulla. Donec quis mi eu diam pulvinar vehicula eu non orci. Maecenas tincidunt lobortis lectus, et tempor lorem suscipit eget. Donec luctus lobortis blandit. Etiam tincidunt sit amet turpis a commodo. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse a tortor a augue sollicitudin gravida. Aenean fermentum odio turpis. Integer tincidunt augue nulla, et ornare metus auctor at. Pellentesque tincidunt aliquam metus, feugiat euismod enim bibendum non. Ut eget risus vehicula, ultricies dui nec, aliquam libero. Curabitur quis malesuada arcu.
Nunc egestas mollis ligula, ut bibendum justo dignissim at. Cras pharetra posuere urna, ut venenatis turpis. Proin placerat, lorem a lacinia maximus, sem nulla tristique purus, non feugiat massa lorem sit amet quam. Nam ullamcorper justo sit amet metus convallis, ut egestas nisl bibendum. Aliquam ut neque nec diam auctor condimentum. Proin ornare diam dolor. Vestibulum vel faucibus ex. In vitae sapien sagittis, tincidunt dolor sed, tempor dolor. Sed vitae efficitur magna. Fusce eget nisl id est pharetra mattis. Integer eget venenatis dui, eget congue metus. Proin vitae arcu condimentum orci fermentum mollis. Praesent enim metus, ullamcorper sit amet fringilla ac, congue eget urna.
Aliquam vestibulum dolor id purus euismod, eu vehicula diam tincidunt. Phasellus eget pellentesque mi. Vivamus imperdiet orci vitae risus tempor, sit amet molestie turpis elementum. Vivamus dictum dapibus mauris eu lacinia. Suspendisse dignissim arcu et dignissim eleifend. Pellentesque dapibus commodo tellus. Duis ac metus semper, viverra justo eu, consequat ligula. Duis rhoncus justo lectus, sed porta est condimentum in. Vestibulum posuere augue non arcu porttitor, eget porta massa eleifend. Nulla ut felis ullamcorper, vulputate mauris ut, laoreet nisl. Suspendisse eget arcu id tortor aliquet ullamcorper. Vivamus lacinia auctor mauris vel semper. Aliquam ut metus vel ante posuere convallis non a augue. Integer ac mauris vitae erat sollicitudin suscipit.
Aenean sit amet purus luctus, convallis velit vel, fermentum erat. Morbi lobortis ipsum vel leo scelerisque dapibus. Nulla eu semper sapien. Vivamus ultrices maximus tortor, ac dictum arcu ornare id. Curabitur sagittis ultricies nisi. Maecenas ultrices augue et lectus suscipit suscipit sit amet condimentum urna. Ut sagittis nunc in libero pharetra, eget commodo arcu hendrerit. Aenean ut ultrices nunc, vel pretium leo. Sed ultrices pellentesque nisl nec placerat. 
Nam nec libero lacinia, tempus ipsum vitae, dignissim odio. Aliquam sodales varius odio, ut pellentesque elit ultrices ut. Nulla luctus placerat porttitor. Phasellus quis pellentesque tellus. Sed eu urna sem. Nulla ornare molestie sapien posuere malesuada. Maecenas eleifend et ante quis auctor. Ut eu lacus volutpat, accumsan mauris a, pretium dolor.
Mauris ornare sapien risus, consectetur interdum dui condimentum aliquam. Nam vel ornare odio, vitae vestibulum sapien. Cras fermentum sagittis dignissim. Nam mattis imperdiet nunc, et egestas dui fringilla id. Quisque at justo sit amet diam tempor iaculis. Curabitur augue dolor, vestibulum rhoncus facilisis at, euismod id urna. Morbi tincidunt elit id elit venenatis varius. Phasellus auctor augue ut nunc mollis luctus. Phasellus suscipit ex maximus volutpat ultricies. Sed molestie nunc quis nunc venenatis volutpat.
Nam facilisis, risus in convallis condimentum, tortor augue dignissim justo, at interdum felis lacus quis risus. Cras vel condimentum quam. Nulla facilisi. Proin tempor fringilla felis, vel blandit ante auctor a. Pellentesque at lacus egestas, mollis magna a, ullamcorper ipsum. Donec accumsan purus non laoreet eleifend. Nullam quis lorem efficitur, placerat purus ut, lacinia tellus. Proin vel ante vitae erat aliquet blandit. Phasellus imperdiet, sapien sit amet dapibus interdum, magna leo dignissim felis, et finibus orci dolor at felis. Donec eleifend fermentum leo vitae consectetur. Duis placerat ante tortor, non porttitor lacus facilisis in. Nulla sollicitudin in tellus eu tincidunt.
Vivamus finibus ac quam ullamcorper maximus. Aenean nibh felis, imperdiet ac tempor sed, maximus et mauris. Nam eget vehicula velit. Fusce vestibulum lacinia commodo. Aliquam et interdum diam. Morbi malesuada elit quis ligula posuere condimentum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer blandit mauris vitae tellus tristique pulvinar. Curabitur ut ornare ex, et commodo orci. Nunc tempus elit at egestas faucibus. Suspendisse tellus nunc, ultricies at viverra vel, rhoncus eget risus. Nam vel neque at eros commodo bibendum. Donec pretium tristique tempor. Sed ornare lacus eget quam gravida rhoncus. Vivamus nec quam a mi dignissim bibendum.
Curabitur lobortis facilisis magna quis pulvinar. Nunc aliquet, felis quis lobortis aliquet, odio orci consectetur quam, sed commodo ex enim a velit. Praesent vel consectetur massa, sed hendrerit augue. Nam tincidunt ut lacus sit amet convallis. Nam maximus elit quis lectus porta posuere. Quisque tortor leo, elementum eget eros laoreet, ultricies egestas nisl. Etiam fermentum lacinia sem, nec placerat turpis. Cras eu enim id metus luctus ornare. Maecenas elementum est non nulla consectetur, et convallis sapien pretium. Nulla aliquam, nunc sed luctus suscipit, tellus arcu laoreet nibh, feugiat eleifend turpis libero eget nunc. Vivamus maximus ligula sed nulla tincidunt, eget imperdiet velit bibendum. Vestibulum diam tortor, faucibus non nisi quis, elementum accumsan mauris. Sed tempus viverra vestibulum. Proin hendrerit, elit vel imperdiet tincidunt, risus nisi facilisis neque, vel bibendum ligula orci id odio.
Integer vehicula ipsum a sem elementum, vitae volutpat nibh tincidunt. Nulla gravida nisi et odio venenatis, vitae auctor lorem hendrerit. Vestibulum aliquet massa vel tristique maximus. Quisque auctor eleifend felis. Nunc vel dictum diam. Nulla maximus maximus ligula, vel molestie dui. Pellentesque vel porta lorem. Phasellus quis dolor vel mi condimentum lacinia id vel arcu. Sed fermentum vel orci ut volutpat. Suspendisse mollis faucibus turpis, nec ullamcorper sem tincidunt quis. Vestibulum gravida arcu non purus pulvinar luctus. In vitae metus sed odio sagittis dapibus eget in lacus. Aliquam mauris massa, ultrices at elit vitae, semper congue lacus.
Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Quisque in purus sagittis, scelerisque ligula sed, semper tellus. Maecenas scelerisque blandit massa. Vivamus porta sed leo at malesuada. Pellentesque sollicitudin, nisi eget cursus aliquet, lorem turpis fringilla purus, sit amet lacinia erat urna sed leo. Sed vulputate metus ligula, id posuere purus mattis sed. Curabitur dolor diam, rhoncus et eros nec, luctus semper quam. Nulla vitae gravida ligula. Quisque mattis non libero eget semper. Pellentesque lacinia egestas enim, vitae vehicula ipsum tempor at. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
Fusce blandit mi nec nisi imperdiet malesuada. Donec facilisis rutrum gravida. Mauris ultricies risus ut justo iaculis bibendum. Fusce sed ligula ultrices, convallis velit sit amet, tincidunt nisi. Fusce cursus suscipit justo, quis vehicula ipsum porttitor in. Pellentesque bibendum, urna at pharetra ornare, neque mauris porta est, bibendum faucibus ex dui nec metus. Sed justo nibh, blandit non nibh ac, dignissim sagittis est. Suspendisse potenti. In eget congue elit, id ornare diam. In quis aliquet mauris, vitae pellentesque turpis. Integer rhoncus quam id magna lobortis, sed hendrerit est bibendum. Nulla mollis lectus et libero vulputate, nec sagittis felis venenatis.
Fusce leo neque, efficitur et lorem sit amet, elementum consequat est. Aliquam erat volutpat. Sed tincidunt nisi eget sollicitudin euismod. Quisque iaculis erat et erat dignissim suscipit. Suspendisse potenti. Nullam est erat, ultrices quis tincidunt at, condimentum et risus. Cras congue ligula ac fermentum malesuada. Donec in consequat lectus. Curabitur sodales efficitur fringilla. Suspendisse sit amet libero vel libero molestie vulputate. Praesent sit amet nisi vitae magna accumsan iaculis. Duis sit amet scelerisque erat. Nunc blandit mollis sapien, sit amet hendrerit lorem imperdiet sed. Nunc sit amet consequat velit. Nulla scelerisque est id risus auctor, vehicula molestie dui auctor.
Sed pretium varius libero, quis iaculis turpis congue quis. Vivamus ut finibus lacus. In euismod elit est, vel gravida ipsum facilisis eu. In consectetur est sed odio luctus, at sollicitudin mi scelerisque. Suspendisse vitae cursus erat. Pellentesque erat ex, consequat eu nisi et, tempor rutrum orci. Praesent non est est. Aenean elit enim, tincidunt sed faucibus eu, convallis eget lectus. Cras aliquet quam a ante ornare eleifend.
Fusce sed libero nisi. Nulla feugiat tempus orci, in molestie lectus lobortis vel. In egestas erat massa, a semper lorem iaculis sit amet. Nunc hendrerit enim at lectus lacinia, id condimentum dui rutrum. Ut eget nulla venenatis, feugiat ex ac, auctor lacus. Vestibulum maximus dolor ornare justo suscipit, sit amet elementum metus feugiat. Aliquam ac lacus eget enim luctus elementum et at augue. Pellentesque cursus malesuada erat, sed sodales ante tristique et. Aenean ut consequat metus. Ut aliquet augue a justo porta, convallis rhoncus nunc venenatis. Proin auctor ante ut dolor faucibus scelerisque vitae nec arcu. Sed id molestie massa, non egestas nibh. Ut eget nibh neque. In a enim quis lorem sagittis tempus sit amet et massa. Quisque eget leo semper, mattis est ac, tempus neque. Maecenas iaculis sapien vel nisl faucibus aliquet.
Phasellus vestibulum elit est, a congue mi varius vel. Suspendisse ornare nibh nulla, eget egestas turpis commodo sit amet. Curabitur at lectus at quam faucibus eleifend non ac ex. Morbi scelerisque lacinia risus, a pulvinar ipsum dapibus condimentum. Maecenas dignissim rhoncus arcu ac efficitur. Proin dui orci, mattis et dapibus id, commodo id arcu. Maecenas pretium maximus risus. Etiam ac egestas elit, eget ultricies nunc. Duis sodales massa tellus, id laoreet purus aliquam in. Donec dapibus accumsan erat et eleifend. Nulla quam est, hendrerit et vestibulum vitae, hendrerit eu ex. 
'''
    def clean_text(txt):
        txt = ''.join(w for w in txt if w != ',')
        txt = ''.join(w for w in txt if w != '.')
        txt = ''.join(w for w in txt if w != '\n')
        return txt.lower()
        
    sample_text = clean_text(sample_text)

    word_counter = Counter(sample_text.split(' '))
    print(word_counter.most_common(10))
    
    words = re.findall(r'\w+', sample_text)
    bigram_counter = Counter(zip(words, words[1:]))
    print(bigram_counter.most_common(10))

    # sentence_len = 4
    # sentence = random.sample(sample_text.split(' '), sentence_len)
    # sentence = clean_text('Nunc fermentum lorem nec felis volutpat ut tincidunt dui tristique')
    sentence = clean_text('amet elementum consequat est Aliquam erat volutpat')
    sentence = sentence.split(' ')
    print(sentence)
    print(f'Probability: {language_model(sentence, word_counter, bigram_counter)}')


if __name__ == '__main__':
    main()