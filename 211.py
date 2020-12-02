"""
///////////////////////// TOP OF FILE COMMENT BLOCK ////////////////////////////
//
// Title:           Invalide model - 211passiv uden invalide
//
// Author:          Peter Pommergård Lind
// Email:           ppl@pfa.dk
// Encoding:        utf-8
///////////////////////////////// CITATIONS ////////////////////////////////////
//
// Edlund MVS
//
/////////////////////////////// 80 COLUMNS WIDE ////////////////////////////////
"""
###########
# Libraries
###########
import pandas
import numpy as np
#############
## Functions
#############
# Integration
def simpson(a,b,f):
  integral = 0 #integral value
  if (b==a):
    return 0
  elif (b==a+1):
    integral += (f(a)+4*f(a+0.5)+f(b))
  else:
    integral += f(a)
    integral += f(b)
    for i in range(a,b):
      integral += 2*f(i)
    for i in range((a+1),b):
      integral += 4/6*f(i + 0.5)
  return (integral/6)

def laplace(a,b,f):
  integral = 0
  if a==b:
    return 0
  elif b==(a+1):
    integral +=f(a)/2
    integral +=f(b)/2
  else:
    integral +=f(a)/2
    integral +=f(b)/2
    for i in range(a+1,b):
      integral += f(i)
  return integral

def muAd(alder,år):
  "Simple interpolation of muAD by rounding age to nearest int"
  if (alder%1==0):
    mu = intensitet[alder] * (1-trend[alder])**(år-2017)
  else:
    alder = round(alder)
    mu = intensitet[alder] * (1-trend[alder])**(år-2017)
  return(mu)


############
# Parameters
###########
n = 64 #pensionsalder
muData = pandas.read_excel(r'./data/muAD.xlsx')
intensitet = muData.Intensitet
trend = muData.Forbedring
år=2020
alder = 39
i=0.01
#####################
# Check funktioner
#######################
def a(x):
  return x
print("Simpson Integration test: ", simpson(0,10,a))
print("Laplace Integration test: ", laplace(0,10,a))
#double integral
#test double integral
def doubleInt(g, n):
  def f1(y):
    return 1
  
  def f2(tau):
    return laplace(g, tau, f1)
  
  return laplace(g,n, f2)

print(doubleInt(0,9))

def doubleInt(g, n):
  def f1(y):
    return 1
  
  def f2(tau):
    return simpson(g, tau, f1)
  
  return simpson(g,n, f2)
################################################
# Simpel liv-død model - 211 passiv med u17 dødeligheder fra PFA tekniske grundlag
################################################


def passiv211a(g,n,år, r):
  """[Find the expected contributions to "opsat livrente"]
  Args:
      g ([int]): [alder ved første udbetaling]
      n ([int]): [sidste udbetalingsdato]
      år ([int]): year of udbetalingsstart
      r ([float]): [interest rate minus "sikkerhedstillæg"]
  """
  def f1(alder):
    # Inner integrand
    return (r+muAd(alder,år+(alder-g))) 
  def f2(tau):
    #second integrand
    return np.exp(-laplace(g,tau,f1))
  return laplace(g,n,f2)

print("Passiv 211: ", passiv211a(g=64,n=110,år=2045, r=0))
#####################################
# Aktiv uden præmiefritagelse
# ####################################  
def aktivUPræmie(g,n,år, r):
  """[Find the expected contributions to "opsat livrente"]
  Args:
      g ([int]): [alder ved beregningsdato]
      n ([int]): [sidste udbetalingsdato]
      år ([int]): year of udbetalingsstart
      r ([float]): [interest rate minus "sikkerhedstillæg"]
  """
  def f1(alder):
    # Inner integrand
    return (r+muAd(alder,år+(alder-g))) 
  def f2(tau):
    #second integrand
    return np.exp(-laplace(g,tau,f1))
  return laplace(g,n,f2)

print("aktiv uden præmiefritagelse", aktivUPræmie(g=39,n=64,år=2020, r=0))
  
#####################################
# Aktiv med præmiefritagelse
# ####################################  
def aktivMPræmie(g,n,år, r):
  TODO
  """[Find the expected contributions to "opsat livrente"]
  Args:
      g ([int]): [alder ved beregningsdato]
      n ([int]): [sidste udbetalingsdato]
      år ([int]): year of udbetalingsstart
      r ([float]): [interest rate minus "sikkerhedstillæg"]
  """
  def f1(alder):
    # Inner integrand
    return (r+muAd(alder,år+(alder-g))) 
  def f2(tau):
    #second integrand
    return np.exp(-laplace(g,tau,f1))
  return laplace(g,n,f2)

print("aktiv uden præmiefritagelse", aktivUPræmie(g=39,n=64,år=2020, r=0))