/*
 * This file was automatically generated by EvoSuite
 * Mon Sep 11 18:43:14 GMT 2017
 */

package org.apache.commons.cli;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Option;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class CommandLine_ESTest extends CommandLine_ESTest_scaffolding {
  /**
   * 1. Creates a new CommandLine and adds arg ""
   */
  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      commandLine0.addArg("");
  }

  /**
   * 1. Creates a new Builder and a new Option
   * 2. Creates a new Builder using addOption of "commandLine_Builder0" with
   *    argument "option0".
   * 3. Creates a new CommandLine using build of commandLine_Builder1 and checks
   *    if it has option "W".
   */
  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("W", "N `");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      boolean boolean0 = commandLine0.hasOption('W');
      assertTrue(boolean0);
  }

  /**
   * 1. Creates a new CommandLine, adds new Option to it and
   *    checks if its Options is not null.
   */
  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      Option option0 = new Option("", false, "");
      commandLine0.addOption(option0);
      Option[] optionArray0 = commandLine0.getOptions();
      assertNotNull(optionArray0);
  }
  
  /**
   * 1. 
   */
  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.setArgs(2);
      option0.addValueForProcessing((String) null);
      String[] stringArray0 = commandLine0.getOptionValues('k');
      assertNotNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      String string0 = commandLine0.getOptionValue("&b}dG 6{FZOpq6", (String) null);
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      String string0 = commandLine0.getOptionValue("", "");
      assertEquals("", string0);
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      String string0 = commandLine0.getOptionValue('', (String) null);
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      String string0 = commandLine0.getOptionValue('I', "");
      assertEquals("", string0);
      assertNotNull(string0);
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      commandLine_Builder0.addArg("e|^G");
      String[] stringArray0 = commandLine0.getArgs();
      assertNotNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      commandLine_Builder0.addArg("");
      CommandLine commandLine0 = commandLine_Builder0.build();
      List<String> list0 = commandLine0.getArgList();
      assertFalse(list0.isEmpty());
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      commandLine0.addOption((Option) null);
      // Undeclared exception!
      try { 
        commandLine0.hasOption("");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      commandLine_Builder0.addOption((Option) null);
      CommandLine commandLine0 = commandLine_Builder0.build();
      // Undeclared exception!
      try { 
        commandLine0.hasOption('Q');
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("W", "N `");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      // Undeclared exception!
      try { 
        commandLine0.getParsedOptionValue((String) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      commandLine_Builder0.addOption((Option) null);
      CommandLine commandLine0 = commandLine_Builder0.build();
      // Undeclared exception!
      try { 
        commandLine0.getOptionValues("The addValue method is not intended for client use. Subclasses should use the addValueForProcessing method instead. ");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      commandLine0.addOption((Option) null);
      // Undeclared exception!
      try { 
        commandLine0.getOptionValues(')');
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      Option option0 = new Option((String) null, " :: ", false, (String) null);
      commandLine0.addOption(option0);
      // Undeclared exception!
      try { 
        commandLine0.getOptionValue((String) null, "v8[`:c");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test16()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      Option option0 = new Option("", true, "");
      commandLine0.addOption(option0);
      // Undeclared exception!
      try { 
        commandLine0.getOptionValue((String) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
      }
  }

  @Test(timeout = 4000)
  public void test17()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      commandLine_Builder0.addOption((Option) null);
      CommandLine commandLine0 = commandLine_Builder0.build();
      // Undeclared exception!
      try { 
        commandLine0.getOptionValue('y', "<I_E^Z");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test18()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      commandLine0.addOption((Option) null);
      // Undeclared exception!
      try { 
        commandLine0.getOptionValue('F');
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test19()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      commandLine_Builder0.addOption((Option) null);
      CommandLine commandLine0 = commandLine_Builder0.build();
      // Undeclared exception!
      try { 
        commandLine0.getOptionObject("true");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test20()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption((Option) null);
      CommandLine commandLine0 = commandLine_Builder1.build();
      // Undeclared exception!
      try { 
        commandLine0.getOptionObject('U');
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("org.apache.commons.cli.CommandLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test21()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      String string0 = commandLine0.getOptionValue("e", "=99yyB,\"LU");
      assertEquals("=99yyB,\"LU", string0);
      assertNotNull(string0);
  }

  @Test(timeout = 4000)
  public void test22()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("t9dH", true, "P<c#iVfU`4fYFatr7");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.addValueForProcessing("Cannot add value, list full.");
      String[] stringArray0 = commandLine0.getOptionValues("t9dH");
      assertNotNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test23()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("", ">M+Lv,ll", true, (String) null);
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      String[] stringArray0 = commandLine0.getOptionValues(">M+Lv,ll");
      assertNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test24()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      String string0 = commandLine0.getOptionValue("");
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test25()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "e", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.setArgs(11);
      option0.addValueForProcessing("W");
      String string0 = commandLine0.getOptionValue("e");
      assertEquals("W", string0);
  }

  @Test(timeout = 4000)
  public void test26()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "e", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.setArgs(11);
      option0.addValueForProcessing("W");
      Object object0 = commandLine0.getParsedOptionValue("k");
      assertEquals("W", object0);
      assertNotNull(object0);
  }

  @Test(timeout = 4000)
  public void test27()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      Object object0 = commandLine0.getParsedOptionValue("k");
      assertNull(object0);
  }

  @Test(timeout = 4000)
  public void test28()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      Object object0 = commandLine0.getParsedOptionValue("");
      assertNull(object0);
  }

  @Test(timeout = 4000)
  public void test29()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      boolean boolean0 = commandLine0.hasOption("*");
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void test30()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", true, "");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.addValueForProcessing("W");
      Properties properties0 = commandLine0.getOptionProperties("");
      assertFalse(properties0.isEmpty());
  }

  @Test(timeout = 4000)
  public void test31()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.setArgs(2);
      option0.addValueForProcessing((String) null);
      option0.addValueForProcessing("W");
      // Undeclared exception!
      try { 
        commandLine0.getOptionProperties("");
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("java.util.Hashtable", e);
      }
  }

  @Test(timeout = 4000)
  public void test32()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      Properties properties0 = commandLine0.getOptionProperties("");
      assertTrue(properties0.isEmpty());
  }

  @Test(timeout = 4000)
  public void test33()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "e", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      Properties properties0 = commandLine0.getOptionProperties("k");
      assertEquals(0, properties0.size());
  }

  @Test(timeout = 4000)
  public void test34()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("t9dH", true, "P<c#iVfU`4fYFatr7");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      Properties properties0 = commandLine0.getOptionProperties("-gGU&*B+UX}X8k'6.7U");
      assertEquals(0, properties0.size());
  }

  @Test(timeout = 4000)
  public void test35()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("t9dH", true, "t9dH");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.addValueForProcessing("Cannot add value, list full.");
      String string0 = commandLine0.getOptionValue("t9dH", "t9dH");
      assertEquals("Cannot add value, list full.", string0);
  }

  @Test(timeout = 4000)
  public void test36()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("t9dH", true, "P<c#iVfU`4fYFatr7");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      Object object0 = commandLine0.getOptionObject('L');
      assertNull(object0);
  }

  @Test(timeout = 4000)
  public void test37()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      String[] stringArray0 = commandLine0.getOptionValues("25V(S");
      assertNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test38()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("t9dH", true, "P<c#iVfU`4fYFatr7");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      option0.addValueForProcessing("Cannot add value, list full.");
      Object object0 = commandLine0.getOptionObject("t9dH");
      assertEquals("Cannot add value, list full.", object0);
      assertNotNull(object0);
  }

  @Test(timeout = 4000)
  public void test39()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("", ">M+Lv,ll", true, (String) null);
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      boolean boolean0 = commandLine0.hasOption("");
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void test40()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      String[] stringArray0 = commandLine0.getArgs();
      assertNotNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test41()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      String string0 = commandLine0.getOptionValue('_');
      assertNull(string0);
  }

  @Test(timeout = 4000)
  public void test42()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      String[] stringArray0 = commandLine0.getOptionValues('k');
      assertNull(stringArray0);
  }

  @Test(timeout = 4000)
  public void test43()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      Option[] optionArray0 = commandLine0.getOptions();
      assertNotNull(optionArray0);
  }

  @Test(timeout = 4000)
  public void test44()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      Object object0 = commandLine0.getOptionObject("");
      assertNull(object0);
  }

  @Test(timeout = 4000)
  public void test45()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      List<String> list0 = commandLine0.getArgList();
      assertEquals(0, list0.size());
  }

  @Test(timeout = 4000)
  public void test46()  throws Throwable  {
      CommandLine commandLine0 = new CommandLine();
      String string0 = commandLine0.getOptionValue('C', ")G^]K$}4#");
      assertEquals(")G^]K$}4#", string0);
      assertNotNull(string0);
  }

  @Test(timeout = 4000)
  public void test47()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      Iterator<Option> iterator0 = commandLine0.iterator();
      assertNotNull(iterator0);
  }

  @Test(timeout = 4000)
  public void test48()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      CommandLine commandLine0 = commandLine_Builder0.build();
      boolean boolean0 = commandLine0.hasOption('Z');
      assertFalse(boolean0);
  }

  @Test(timeout = 4000)
  public void test49()  throws Throwable  {
      CommandLine.Builder commandLine_Builder0 = new CommandLine.Builder();
      Option option0 = new Option("k", "", false, "v");
      CommandLine.Builder commandLine_Builder1 = commandLine_Builder0.addOption(option0);
      CommandLine commandLine0 = commandLine_Builder1.build();
      Object object0 = commandLine0.getOptionObject("");
      assertNull(object0);
  }
}
