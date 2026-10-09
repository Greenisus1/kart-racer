import unittest,random,collections
import game
modules={'kart-racer':game}
class Tests(unittest.TestCase):
 def test_racer(self):
  g=modules['kart-racer'].Racer();g.objects=[(1,0,'coin')];g.speed=38;g.step(.1);self.assertEqual(g.score,1)
 def test_racer_crash(self):
  g=modules['kart-racer'].Racer();g.objects=[(1,0,'rival')];g.speed=38;g.step(.1);self.assertEqual(g.health,4)
 def test_racer_bounds(self):
  g=modules['kart-racer'].Racer()
  for _ in range(200):g.step(.1,1,True)
  self.assertLessEqual(g.x,1.2);self.assertGreaterEqual(g.speed,0)
if __name__=="__main__":unittest.main()
